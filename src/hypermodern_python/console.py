# src/hypermodern_python/console.py
import textwrap

import click
import requests

from . import __version__, wikipedia


API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

@click.command()
@click.option(
    "--language",
    "-l",
    default = "vi",
    help = "Language edition of Wikipedia",
    metavar = "LANG",
    show_default = True,
)
@click.version_option(version = __version__)
def main(language):
    """The hypermodern Python project."""
    data = wikipedia.random_page(language = language)

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))
