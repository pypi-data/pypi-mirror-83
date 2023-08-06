from typing import List

import click

from sym.cli.helpers.check.runner import must_run_all

from ..decorators import loses_interactivity
from ..helpers.global_options import GlobalOptions
from .sym import sym


@sym.command(hidden=True, short_help="runs a series of checks against a sym resource")
@click.make_pass_decorator(GlobalOptions)
@click.argument("resource")
@click.option("--instance", multiple=True, default=[])
@loses_interactivity
def check(options: GlobalOptions, resource: str, instance: List[str]):
    must_run_all(options, resource, instance)
