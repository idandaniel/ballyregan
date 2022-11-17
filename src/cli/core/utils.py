from typing import List

import typer
from prettytable import ALL
from prettytable.colortable import ColorTable, Themes

from ballyregan import Proxy
from cli.core.config import OutputFormats


def proxies_to_table(proxies: List[Proxy]) -> ColorTable:
    proxy_field_names = Proxy.schema(False).get("properties").keys()
    proxies_table = ColorTable(
        theme=Themes.OCEAN,
        field_names=['full address', *proxy_field_names],
        padding_width=3,
        hrules=ALL
    )
    proxies_table.add_rows([
        [str(proxy), *proxy.dict().values()]
        for proxy in proxies
    ])
    return proxies_table


def proxies_to_json_list(proxies: List[Proxy]) -> List[dict]:
    return [proxy.dict() for proxy in proxies]


def print_proxies(proxies: List[Proxy], output_format: OutputFormats = OutputFormats.TABLE) -> None:
    format_methods_mapper = {
        'json': proxies_to_json_list,
        'table': proxies_to_table
    }
    formatted_proxies = format_methods_mapper[output_format](proxies)
    typer.echo(formatted_proxies)
