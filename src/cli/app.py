from typing import List

import typer
from cli.core.config import OutputFormats
from cli.core.utils import print_proxies

from ballyregan import ProxyFetcher
from ballyregan.core.exceptions import ProxyException
from ballyregan.models import Protocols, Anonymities


app = typer.Typer()

fetcher = ProxyFetcher()


@app.command(help="Get Proxies.")
def get(
    protocols: List[Protocols] = typer.Option(
        [],
        '--protocol', '-p',
        help='Search proxies only with the given protocols.'
    ),
    anonymities: List[Anonymities] = typer.Option(
        [],
        '--anonymity', '-a',
        help='Search proxies only with the given anonymities.'
    ),
    limit: int = typer.Option(
        1,
        '--limit', '-l',
        min=1,
        help='Amount of proxies to fetch.'
    ),
    all: bool = typer.Option(
        False,
        '--all',
        help='Gather all proxies it can find.'
    ),
    output_format: OutputFormats = typer.Option(
        OutputFormats.TABLE.value,
        '--output', '-o',
        help='Output format of proxies.'
    )
) -> None:
    if all:
        limit = 0
    try:
        proxies = fetcher.get(
            protocols=protocols,
            anonymities=anonymities,
            limit=limit
        )
    except ProxyException as e:
        typer.echo(message=e, err=True)
    except Exception as e:
        typer.echo(message=f'UNKNOWN ERROR - {e}', err=True)
    else:
        print_proxies(proxies, output_format=output_format)


@app.callback()
def callback(
        debug: bool = typer.Option(False, '--debug')
):
    fetcher.debug = debug


def run() -> None:
    app()
