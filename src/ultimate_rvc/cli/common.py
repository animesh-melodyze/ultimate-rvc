"""Common utilities for the CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ultimate_rvc.typing_extra import (
    AudioExt,
    AudioNormalizationMode,
    AudioSplitMethod,
    DeviceType,
    EmbedderModel,
    F0Method,
    IndexAlgorithm,
    PrecisionType,
    PretrainedType,
    SampleRate,
    TrainingSampleRate,
    Vocoder,
)

if TYPE_CHECKING:
    from pathlib import Path

# Shared CLI state populated by the root Typer callback in cli/main.py and
# read by individual subcommands. Avoids passing Typer Context through every
# call site.
cli_state: dict[str, object] = {"device": "auto", "json_output": False}

HD_MP3_BITRATE = "256k"
HD_MP3_SAMPLE_RATE = 48_000
HD_MP3_CHANNELS = 2


def to_hd_mp3(wav_path: Path) -> Path:
    """
    Re-encode a WAV file to HD MP3 (256 kbps, 48 kHz, stereo).

    Writes the MP3 next to the source WAV with the same stem.

    Parameters
    ----------
    wav_path : Path
        Path to the source WAV file.

    Returns
    -------
    Path
        Path to the resulting MP3 file.

    """
    from pydub import AudioSegment

    audio = AudioSegment.from_wav(str(wav_path))
    audio = audio.set_frame_rate(HD_MP3_SAMPLE_RATE).set_channels(HD_MP3_CHANNELS)
    mp3_path = wav_path.with_suffix(".mp3")
    audio.export(str(mp3_path), format="mp3", bitrate=HD_MP3_BITRATE)
    return mp3_path


def format_duration(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.

    Parameters
    ----------
    seconds : float
        The duration in seconds.

    Returns
    -------
    str
        The formatted duration

    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{int(hours)} hours, {int(minutes)} minutes, and {seconds:.2f} seconds"
    if minutes > 0:
        return f"{int(minutes)} minutes and {seconds:.2f} seconds"
    return f"{seconds:.2f} seconds"


def complete_name(incomplete: str, enumeration: list[str]) -> list[str]:
    """
    Return a list of names that start with the incomplete string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.
    enumeration : list[str]
        The list of names to complete from.

    Returns
    -------
    list[str]
        The list of names that start with the incomplete string.

    """
    return [name for name in list(enumeration) if name.startswith(incomplete)]


def complete_audio_ext(incomplete: str) -> list[str]:
    """
    Return a list of audio extensions that start with the incomplete
    string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of audio extensions that start with the incomplete
        string.

    """
    return complete_name(incomplete, list(AudioExt))


def complete_f0_method(incomplete: str) -> list[str]:
    """
    Return a list of F0 methods that start with the incomplete string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of F0 methods that start with the incomplete string.

    """
    return complete_name(incomplete, list(F0Method))


def complete_embedder_model(incomplete: str) -> list[str]:
    """
    Return a list of embedder models that start with the incomplete
    string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of embedder models that start with the incomplete
        string.

    """
    return complete_name(incomplete, list(EmbedderModel))


def complete_audio_split_method(incomplete: str) -> list[str]:
    """
    Return a list of audio split methods that start with the incomplete
    string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of audio split methods that start with the incomplete
        string.

    """
    return complete_name(incomplete, list(AudioSplitMethod))


def complete_sample_rate(incomplete: str) -> list[str]:
    """
    Return a list of sample rates that start with the incomplete string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of sample rates that start with the incomplete string.

    """
    return complete_name(incomplete, [str(sr) for sr in SampleRate])


def complete_training_sample_rate(incomplete: str) -> list[str]:
    """
    Return a list of training sample rates that start with the
    incomplete string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of training sample rates that start with the incomplete
        string.

    """
    return complete_name(incomplete, [str(sr) for sr in TrainingSampleRate])


def complete_normalization_mode(incomplete: str) -> list[str]:
    """
    Return a list of audio normalization modes that start with the
    incomplete string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of audio normalization modes that start with the
        incomplete string.

    """
    return complete_name(incomplete, list(AudioNormalizationMode))


def complete_vocoder(incomplete: str) -> list[str]:
    """
    Return a list of vocoders that start with the incomplete string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of vocoders that start with the incomplete string.

    """
    return complete_name(incomplete, list(Vocoder))


def complete_index_algorithm(incomplete: str) -> list[str]:
    """
    Return a list of index algorithms that start with the incomplete
    string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of index algorithms that start with the incomplete
        string.

    """
    return complete_name(incomplete, list(IndexAlgorithm))


def complete_device_type(incomplete: str) -> list[str]:
    """
    Return a list of device types that start with the incomplete
    string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of device types that start with the incomplete
        string.

    """
    return complete_name(incomplete, list(DeviceType))


def complete_precision_type(incomplete: str) -> list[str]:
    """
    Return a list of precision types that start with the incomplete
    string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of precision types that start with the incomplete
        string.

    """
    return complete_name(incomplete, list(PrecisionType))


def complete_pretrained_type(incomplete: str) -> list[str]:
    """
    Return a list of pretrained model types that start with the
    incomplete string.

    Parameters
    ----------
    incomplete : str
        The incomplete string to complete.

    Returns
    -------
    list[str]
        The list of pretrained model types that start with the
        incomplete string.

    """
    return complete_name(incomplete, list(PretrainedType))
