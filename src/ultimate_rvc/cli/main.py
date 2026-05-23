"""
Module which defines the command-line interface for the Ultimate RVC
project.
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Annotated

import typer

from ultimate_rvc.cli.common import cli_state
from ultimate_rvc.cli.generate.main import app as generate_app


class Device(str, Enum):
    """Compute-device selection for the CLI's global --device flag."""

    AUTO = "auto"
    CPU = "cpu"
    CUDA = "cuda"


app = typer.Typer(
    name="urvc-cli",
    no_args_is_help=True,
    help="CLI for the Ultimate RVC project (karaoke vocal-timbre fork)",
    rich_markup_mode="markdown",
)


@app.callback()
def _global_options(
    device: Annotated[
        Device,
        typer.Option(
            "--device",
            case_sensitive=False,
            help=(
                "Compute device. `auto` uses CUDA if available, otherwise CPU."
                " `cpu` forces CPU even when CUDA is present."
            ),
        ),
    ] = Device.AUTO,
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Emit machine-readable JSON on stdout instead of formatted text.",
        ),
    ] = False,
) -> None:
    """Global options applied to every subcommand."""
    cli_state["device"] = device.value
    cli_state["json_output"] = json_output
    # Force CPU by hiding all CUDA devices before torch is imported. Works
    # because torch is lazy-loaded; the env var is read at torch init time.
    if device == Device.CPU:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""


app.add_typer(generate_app)


if __name__ == "__main__":
    app()
