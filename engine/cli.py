import os
from datetime import datetime
from typing import Optional

from pymongo import MongoClient
from engine import __app_name__, __version__

import typer

from engine.scrapper.service import run_scrapper

config = os.environ

app = typer.Typer()


@app.command()
def collect(
        analytic_id: str,
        minutes: int = typer.Option(15, "--minutes", "-m", help="Scrapping tweet that is created m minutes ago", )
):
    error = run_scrapper(analytic_id, minutes)
    if error:
        typer.secho(
            f'Failed to scrapping analytic ${analytic_id}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho("Collecting data is success", fg=typer.colors.GREEN)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show application's version and exit.",
    callback=_version_callback,
    is_eager=True,
)) -> None:
    return
