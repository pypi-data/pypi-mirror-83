import json
import re
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from textwrap import dedent
from typing import Optional, Sequence, Tuple

import boto3
import validators
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError, ConnectionError, WaiterError

from ..decorators import retry
from ..errors import BotoError, CliError, InstanceNotFound, OfflineError
from .config import Config, SymConfigFile
from .params import get_ssh_user
from .threading import first

InstanceIDPattern = re.compile("^i-[a-f0-9]+$")
UnauthorizedError = re.compile(r"UnauthorizedOperation")
RequestExpired = re.compile(r"RequestExpired")


def intercept_boto_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ConnectionError as err:
            raise OfflineError() from err
        except ClientError as err:
            if UnauthorizedError.search(str(err)):
                raise BotoError(
                    err, f"Does your user role have permission to {err.operation_name}?"
                )
            if RequestExpired.search(str(err)):
                raise BotoError(
                    err,
                    f"Your AWS credentials have expired. Try running `sym write-creds` again.",
                )

            raise CliError(str(err)) from err

    return wrapped


def boto_client(saml_client, service):
    creds = saml_client.get_creds()
    return boto3.client(
        service,
        config=BotoConfig(region_name=get_region(saml_client, creds)),
        aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
        aws_session_token=creds.get("AWS_SESSION_TOKEN"),
    )


def get_region(saml_client, creds=None) -> str:
    override = saml_client.options.aws_region
    return override or (creds or saml_client.get_creds()).get("AWS_REGION")


@intercept_boto_errors
def get_regions(saml_client) -> Sequence[str]:
    try:
        client = boto_client(saml_client, "ec2")
        regions = [
            region["RegionName"] for region in client.describe_regions()["Regions"]
        ]
    except ClientError:
        session = boto3.Session()
        regions = session.get_available_regions("ec2")

    return sorted(regions, key=lambda r: ("us" not in r, "eu" not in r, r))


@intercept_boto_errors
def send_ssh_key(saml_client: "SAMLClient", instance: str, ssh_key: SymConfigFile):
    saml_client.dprint("sending SSH key")

    user = get_ssh_user()
    ssm_client = boto_client(saml_client, "ssm")
    # fmt: off
    command = dedent(
        f"""
        #!/bin/bash
        mkdir -p "$(echo ~{user})/.ssh"
        echo "{ssh_key.path.with_suffix('.pub').read_text()}" >> "$(echo ~{user})/.ssh/authorized_keys"
        chown -R {user}:{user} "$(echo ~{user})/.ssh"
        """
    ).strip()
    # fmt: on

    response = ssm_client.send_command(
        InstanceIds=[instance],
        DocumentName="AWS-RunShellScript",
        Comment="SSH Key for Sym",
        Parameters={"commands": command.splitlines()},
    )

    saml_client.dprint(response)

    _wait_for_command(ssm_client, instance, response)


@retry(
    WaiterError,
    count=5,
    delay=1,
    check_ex=lambda ex: ex.last_response["Error"]["Code"] == "InvocationDoesNotExist",
)
def _wait_for_command(ssm_client, instance, response):
    waiter = ssm_client.get_waiter("command_executed")
    waiter.wait(
        InstanceId=instance,
        CommandId=response["Command"]["CommandId"],
        WaiterConfig={"Delay": 1},
    )


@dataclass
class RunningInstance:
    instance_id: str
    region: str

    def __repr__(self):
        return f"{self.instance_id} [{self.region}]"


@intercept_boto_errors
def get_running_instance(
    saml_client,
    *,
    instance_id: Optional[str] = None,
    filter: Optional[Tuple[str, str]] = None,
) -> Optional[RunningInstance]:
    if not instance_id and not filter:
        raise ValueError("must provide instance id or filter to get instance")
    ec2_client = boto_client(saml_client, "ec2")
    saml_client.dprint(
        f"getting instance",
        instance_id=instance_id,
        region=ec2_client.meta.region_name,
        filter=filter,
    )
    try:
        paginator = ec2_client.get_paginator("describe_instances")
        filters = [{"Name": "instance-state-name", "Values": ["running"]}]
        if filter:
            filters.append({"Name": filter[0], "Values": [filter[1]]})
        instance_ids = [instance_id] if instance_id else []
        for response in paginator.paginate(
            Filters=filters,
            InstanceIds=instance_ids,
        ):
            if response["Reservations"]:
                instance = response["Reservations"][0]["Instances"][0]
                return RunningInstance(
                    instance_id=instance["InstanceId"], region=ec2_client.meta.region_name
                )
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
            raise InstanceNotFound(instance_id)
        raise


def find_instance(saml_client, keys, value) -> Optional[str]:
    if (cached := Config.find_instance_by_alias(value)) :
        saml_client.dprint("found cached instance", instance=cached)
        return cached

    saml_client.dprint(f"finding instance", keys=keys, value=value)

    for key in keys:
        result = get_running_instance(saml_client, filter=(key, value))
        if result:
            Config.add_instance_alias(
                result.instance_id,
                alias=value,
                region=result.region,
            )
            return result.instance_id


@intercept_boto_errors
def get_identity(saml_client) -> dict:
    sts_client = boto_client(saml_client, "sts")
    return sts_client.get_caller_identity()


def host_to_instance(saml_client, host: str) -> str:
    saml_client.dprint(f"finding instance: host={host}")

    target = None
    if InstanceIDPattern.match(host):
        result = get_running_instance(saml_client, instance_id=host)
        if result:
            target = result.instance_id

    elif validators.ip_address.ipv4(host):
        target = find_instance(saml_client, ("ip-address", "private-ip-address"), host)
    else:
        target = find_instance(saml_client, ("dns-name", "private-dns-name"), host)

    if not target:
        raise InstanceNotFound(host)

    return target


def search_for_host(saml_client, host: str) -> RunningInstance:
    try:
        instance = host_to_instance(saml_client, host)
        if (region := Config.get_instance(instance)["region"]) :
            return RunningInstance(instance_id=instance, region=region)
    except InstanceNotFound:
        pass
    except KeyError:
        pass

    regions = get_regions(saml_client)

    finder = lambda region: host_to_instance(
        saml_client.clone(options=saml_client.options.clone(aws_region=region)),
        host,
    )
    if (value := first(regions, finder)) :
        return RunningInstance(instance_id=value[1], region=value[0])
    else:
        raise InstanceNotFound(host)


@contextmanager
@intercept_boto_errors
def ssm_session(saml_client, instance: str, port: int):
    ssm_client = boto_client(saml_client, "ssm")
    params = {
        "Target": instance,
        "DocumentName": "AWS-StartSSHSession",
        "Parameters": {"portNumber": [str(port)]},
    }
    response = ssm_client.start_session(**params)
    command = [
        "session-manager-plugin",
        json.dumps(response),
        ssm_client.meta.region_name,
        "StartSession",
        "",
        json.dumps(params),
        ssm_client.meta.endpoint_url,
    ]
    try:
        yield command
    finally:
        ssm_client.terminate_session(SessionId=response["SessionId"])


@intercept_boto_errors
def put_file(saml_client, bucket: str, file_path: Path, object_path: str):
    s3_client = boto_client(saml_client, "s3")
    s3_client.upload_file(
        str(file_path),
        bucket,
        object_path,
        ExtraArgs={"ACL": "bucket-owner-full-control"},
    )
