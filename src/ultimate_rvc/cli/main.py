"""
Module which defines the command-line interface for the Ultimate RVC
project.
"""

from __future__ import annotations

import json
import os
import platform
import sys
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


def _detect_accelerators() -> dict[str, object]:
    """
    Probe the runtime for hardware accelerators usable by Ultimate RVC.

    Returns a dict with platform info, per-accelerator availability, and
    a recommended value for the ``URVC_ACCELERATOR`` install-time env var.
    """
    info: dict[str, object] = {
        "os": platform.system(),
        "arch": platform.machine(),
        "python": platform.python_version(),
    }

    try:
        import torch

        info["torch"] = torch.__version__
        cuda_available = bool(torch.cuda.is_available())
        # torch.version.hip is set when the wheel was built against ROCm.
        rocm_built = getattr(torch.version, "hip", None) is not None
        rocm_available = rocm_built and cuda_available
        mps_available = bool(
            getattr(torch.backends, "mps", None)
            and torch.backends.mps.is_available()
        )
        cuda_devices: list[str] = []
        if cuda_available and not rocm_built:
            cuda_devices = [
                torch.cuda.get_device_name(i)
                for i in range(torch.cuda.device_count())
            ]
        info["torch_import_error"] = None
    except Exception as exc:  # noqa: BLE001 — surface any import-time failure
        info["torch"] = None
        info["torch_import_error"] = f"{type(exc).__name__}: {exc}"
        cuda_available = False
        rocm_available = False
        mps_available = False
        cuda_devices = []

    info["accelerators"] = {
        "cpu": {"available": True},
        "cuda": {"available": cuda_available and not rocm_available,
                 "devices": cuda_devices},
        "rocm": {"available": rocm_available},
        "mps": {"available": mps_available},
    }

    os_name = info["os"]
    if cuda_available and not rocm_available:
        recommended = "cuda"
    elif rocm_available:
        recommended = "rocm"
    else:
        recommended = "cpu"
    info["recommended_urvc_accelerator"] = recommended

    notes: list[str] = []
    if mps_available and recommended == "cpu":
        notes.append(
            "Apple Silicon MPS detected: install with URVC_ACCELERATOR=cpu;"
            " run with `--device auto` to use MPS at inference time.",
        )
    if os_name == "Darwin" and recommended in {"cuda", "rocm"}:
        notes.append("CUDA/ROCm are not supported on macOS.")
    info["notes"] = notes
    return info


@app.command("info")
def info() -> None:
    """
    Show detected accelerators and the recommended `URVC_ACCELERATOR`
    value for this machine.
    """
    data = _detect_accelerators()

    if cli_state.get("json_output"):
        typer.echo(json.dumps(data, indent=2))
        return

    accels = data["accelerators"]  # type: ignore[assignment]
    typer.echo(f"OS:         {data['os']} ({data['arch']})")
    typer.echo(f"Python:     {data['python']}")
    typer.echo(f"PyTorch:    {data['torch'] or 'not importable'}")
    if data["torch_import_error"]:
        typer.echo(f"  import error: {data['torch_import_error']}")
    typer.echo("")
    typer.echo("Accelerators:")
    for name in ("cpu", "cuda", "rocm", "mps"):
        entry = accels[name]  # type: ignore[index]
        status = "available" if entry["available"] else "not available"
        line = f"  {name.upper():<5} {status}"
        devices = entry.get("devices") if isinstance(entry, dict) else None
        if devices:
            line += f"  [{', '.join(devices)}]"
        typer.echo(line)
    typer.echo("")
    typer.echo(
        f"Recommended URVC_ACCELERATOR: {data['recommended_urvc_accelerator']}",
    )
    for note in data["notes"]:  # type: ignore[union-attr]
        typer.echo(f"  note: {note}")

    sys.stdout.flush()


if __name__ == "__main__":
    app()
