from json import dumps

import click

from ..decorators import loses_interactivity, require_login
from ..errors import CliError
from ..helpers import boto
from ..helpers.global_options import GlobalOptions
from ..helpers.options import resource_argument
from .sym import sym


@sym.command(short_help="Get an Instance ID for a host")
@click.option("--json", is_flag=True, hidden=True)
@resource_argument
@click.argument("host")
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_login
def host_to_instance(
    options: GlobalOptions,
    resource: str,
    host: str,
    json: bool,
) -> None:
    client = options.create_saml_client(resource)

    result = boto.search_for_host(client, host)
    if result is None:
        raise CliError(f"instance {host} not found")

    if json:
        click.echo(dumps({"instance": result.instance_id, "region": result.region}))
    else:
        click.echo(result.instance_id)
