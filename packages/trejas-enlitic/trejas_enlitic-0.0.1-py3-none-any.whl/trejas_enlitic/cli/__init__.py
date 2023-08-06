import logging

global logger
logger = logging.getLogger()
logger.setLevel(50)

import click

from trejas_enlitic.utils.log import setup_logging
from trejas_enlitic import version as cli_version, title as cli_title
from trejas_enlitic.functions import display_stats_for_timestamp, ingest_logs
from tabulate import tabulate

logger = setup_logging(logger)


@click.group()
@click.option("--debug", is_flag=True)
@click.pass_context
def cli(ctx: click.core.Context, debug: bool):
    ctx.ensure_object(dict)

    if debug:
        logger.setLevel(10)

    click.echo("Created")


@cli.command("version")
def version() -> None:
    click.echo(cli_title)
    click.echo(cli_version)


@cli.command("report")
@click.option(
    "--log-file", required=True, help="File path to the log file for parsing."
)
@click.option(
    "--timestamp",
    required=True,
    help="Timestamp to use to search. Must be in format -- 2019-08-26 18:41:34+00:00",
)
@click.option("--splits", "-s", help="Add a split.", multiple=True, default=[5, 10, 15])
@click.pass_context
def gen_report(
    ctx: click.core.Context, log_file: str, timestamp: str, splits: list
) -> None:
    with open(log_file) as f:
        data = f.read().splitlines()
    data_df = ingest_logs(data)
    output_df = display_stats_for_timestamp(data_df, timestamp, splits)

    click.echo(tabulate(output_df, headers="keys", tablefmt="psql"))
