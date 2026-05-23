"""
Module which defines functions for initializing the core of the Ultimate
RVC project.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import lazy_loader as lazy

from pathlib import Path

from rich import print as rprint

from ultimate_rvc.common import VOICE_MODELS_DIR
from ultimate_rvc.core.common import FLAG_FILE
from ultimate_rvc.core.manage.models import download_voice_model
from ultimate_rvc.rvc.lib.tools.prerequisites_download import (
    prequisites_download_pipeline,
)

if TYPE_CHECKING:
    import static_sox

else:
    static_sox = lazy.load("static_sox")


def download_sample_models() -> None:
    """Download sample RVC models."""
    named_model_links = [
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Ariana_Grande__RVC_v1.zip", "Ariana Grande"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Adele_RVC.zip", "Adele"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/EdSheeran_RVC.zip", "Ed Sheeran"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Lana_Del_Rey_RVC.zip", "Lana Del Rey"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Taylor_Swift_RVC.zip", "Taylor Swift"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Frank_Sinatra_RVC.zip", "Frank Sinatra"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Sid_Sriram_RVC.zip", "Sid Sriram"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Arijit_Singh_RVC.zip", "Arijit Singh"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Shreya_Ghosal_RVC.zip", "Shreya Ghoshal"),
        ("https://melodyze-public-bucket.s3.ap-south-1.amazonaws.com/rvc_models/Armaan_Malik_RVC.zip", "Armaan Malik"),
    ]
    for model_url, model_name in named_model_links:
        if not Path(VOICE_MODELS_DIR / model_name).is_dir():
            rprint(f"Downloading {model_name}...")
            try:
                download_voice_model(model_url, model_name)
            except Exception as e:  # noqa: BLE001
                rprint(f"Failed to download {model_name}: {e}")


def initialize() -> None:
    """Initialize the Ultimate RVC project."""
    prequisites_download_pipeline(exe=False)
    if not FLAG_FILE.is_file():
        # NOTE we only add_paths so that sox
        # binaries are downloaded as part of initialization.
        static_sox.add_paths(weak=True)
        download_sample_models()
        FLAG_FILE.touch()


if __name__ == "__main__":
    initialize()
