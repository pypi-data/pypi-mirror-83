import json
from typing import Sequence

from sym.cli.helpers.boto import intercept_boto_errors
from sym.cli.saml_clients.saml_client import SAMLClient

from ...errors import BotoError, CliError, InstanceNotFound
from ..boto import boto_client, get_identity, search_for_host
from .model import CheckContext, CheckResult, SymCheck, failure, success


class CallerIdentityCheck(SymCheck):
    def check(self, ctx: CheckContext) -> CheckResult:
        client = ctx.options.create_saml_client(ctx.resource)
        try:
            identity = get_identity(client)
            pretty = json.dumps(identity, indent=4, sort_keys=True)
            return success(f"Successfully got AWS identity:\n{pretty}")
        except CliError as e:
            return failure(f"Unable to get AWS identity: {e.message}")


@intercept_boto_errors
def describe_regions(client: SAMLClient) -> Sequence[str]:
    ec2_client = boto_client(client, "ec2")
    return [region["RegionName"] for region in ec2_client.describe_regions()["Regions"]]


class DescribeRegionsCheck(SymCheck):
    def check(self, ctx: CheckContext) -> CheckResult:
        client = ctx.options.create_saml_client(ctx.resource)
        try:
            ctx.regions = describe_regions(client)
            return success(f"Found {len(ctx.regions)} regions")
        except BotoError as e:
            return failure(f"Unable to describe regions: {e.message}")


class DescribeInstanceCheck(SymCheck):
    def __init__(self, instance: str):
        self.instance = instance

    def check(self, ctx: CheckContext) -> CheckResult:
        client = ctx.options.create_saml_client(ctx.resource)
        try:
            running_instance = search_for_host(client, self.instance)
            if running_instance is None:
                return failure(f"Unable to locate instance {self.instance}")
            return success(
                f"Located instance {running_instance.instance_id} in region {running_instance.region}"
            )
        except InstanceNotFound as e:
            return failure(f"{e.message}")
