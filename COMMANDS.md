# Commands — Install & Run

Quick reference for installing and running this fork. For the fork-vs-upstream
workflow, see [FORK_MANAGEMENT.md](FORK_MANAGEMENT.md).

This fork is CLI-only: vocal-timbre conversion that outputs HD MP3
(256 kbps, 48 kHz, stereo). Supports CPU and CUDA, on Linux, macOS and
Windows.

## Install

The `urvc` (bash) and `urvc.ps1` (PowerShell) launchers handle everything:
uv install, Python download, dependency install. Pick the matching block.

### Linux — GPU (NVIDIA CUDA, default)

```bash
git clone https://github.com/animesh-melodyze/ultimate-rvc.git
cd ultimate-rvc
./urvc install
```

Installs Ubuntu system packages, CUDA 12.8 toolkit, uv, Python 3.13, and
all dependencies with the `cuda` extra.

### Linux — CPU only

```bash
URVC_ACCELERATOR=cpu ./urvc install
```

Skips CUDA toolkit; pulls CPU PyTorch wheels from
`https://download.pytorch.org/whl/cpu`.

### macOS

```bash
git clone https://github.com/animesh-melodyze/ultimate-rvc.git
cd ultimate-rvc
./urvc install
```

Defaults to `cpu` on macOS (CUDA is unavailable on Mac). On Apple Silicon,
PyTorch can pick up MPS at runtime when `--device auto` is used.

> Intel Mac: PyTorch dropped Intel macOS wheels after 2.2.x. This fork pins
> `torch==2.7.1`, which has no Intel Mac wheel — install will fail on
> Intel Macs.

### Windows — GPU (default)

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser   # one-time
git clone https://github.com/animesh-melodyze/ultimate-rvc.git
cd ultimate-rvc
./urvc.ps1 install
```

### Windows — CPU only

```powershell
$env:URVC_ACCELERATOR = "cpu"
./urvc.ps1 install
```

### Docker

```bash
# GPU host (default — uncomment the `devices:` block in docker-compose.yml first)
docker compose -f docker/docker-compose.yml build

# CPU host
URVC_ACCELERATOR=cpu docker compose -f docker/docker-compose.yml build
```

## Run

### Basic conversion

```bash
./urvc cli generate convert-voice <input_vocal> <output_dir> <model_name>
```

Example:

```bash
./urvc cli generate convert-voice ./samples/vocal.wav ./out "Ariana Grande"
```

Output: `./out/21_Voice_Converted_<hash>.mp3`

### Force CPU on a CUDA host

```bash
./urvc cli --device cpu generate convert-voice ./samples/vocal.wav ./out "Adele"
```

### JSON output (for subprocess / automation)

```bash
./urvc cli --json generate convert-voice ./samples/vocal.wav ./out "Ed Sheeran"
```

Stdout (single line):

```json
{"status":"ok","input_path":"...","model":"Ed Sheeran","wav_path":"...","output_path":"....mp3","elapsed_seconds":38.4,"device":"auto"}
```

### Docker run

```bash
docker compose -f docker/docker-compose.yml run --rm ultimate-rvc \
    generate convert-voice /app/audio/vocal.wav /app/audio "Adele"
```

Volumes are mapped to `../models`, `../audio`, `../logs`, `../temp` on the
host (see [docker/docker-compose.yml](docker/docker-compose.yml)).

## Global CLI flags

| Flag | Values | Default | Notes |
| --- | --- | --- | --- |
| `--device` | `auto`, `cpu`, `cuda` | `auto` | `cpu` sets `CUDA_VISIBLE_DEVICES=""` before torch initialises. |
| `--json` | (boolean) | off | Emit one JSON object on stdout instead of formatted text. |

Global flags go **before** the subcommand:

```bash
./urvc cli --device cpu --json generate convert-voice ...
```

## convert-voice options (most useful)

| Option | Default | Notes |
| --- | --- | --- |
| `--n-octaves` | `0` | Pitch shift by octaves. `1` = male→female, `-1` = female→male. |
| `--n-semitones` | `0` | Finer pitch shift. |
| `--f0-method` | `rmvpe` | `rmvpe`, `fcpe`, `crepe`. FCPE is fastest. |
| `--index-rate` | `0.3` | Influence of the model's `.index` file (0..1). |
| `--protect-rate` | `0.33` | Protects consonants from artefacts (0..0.5). |
| `--clean-voice / --no-clean-voice` | off | Apply noise reduction. |
| `--autotune-voice / --no-autotune-voice` | off | Snap pitch to chromatic grid. |
| `--embedder-model` | `contentvec` | `contentvec`, `chinese-hubert-base`, `japanese-hubert-base`, `korean-hubert-base`, `custom`. |
| `--sid` | `0` | Speaker ID (for multi-speaker models). |

Full reference:

```bash
./urvc cli generate convert-voice --help
```

## Other launcher commands

| Command | Purpose |
| --- | --- |
| `./urvc install` | Install deps (see Install section). |
| `./urvc update` | `git pull` the latest commit from your fork. |
| `./urvc uninstall` | Remove `uv/` (Python + venv) and all generated data. Source code stays. |
| `./urvc cli ...` | Run the urvc CLI. |
| `./urvc docs <module> <out_dir>` | Generate Typer docs for a module. |
| `./urvc uv <args>` | Pass-through to the bundled uv binary. |
| `./urvc help` | Show launcher usage. |

## Environment variables

| Variable | Values | Default | Purpose |
| --- | --- | --- | --- |
| `URVC_ACCELERATOR` | `cuda`, `cpu`, `rocm` | `cuda` on Linux/Windows, `cpu` on macOS | Which PyTorch extra to install / use. |
| `URVC_MODELS_DIR` | path | `./models` | Override model storage location. |
| `URVC_AUDIO_DIR` | path | `./audio` | Override audio storage location. |
| `URVC_LOGS_DIR` | path | `./logs` | Override log location. |

## Caching

Each conversion writes an intermediate WAV next to the MP3 in the output
directory. Re-running the **same** input + model + parameters reuses the cached
WAV (skips RVC inference) and just re-encodes the MP3. To force a re-run,
delete the cached `21_Voice_Converted_<hash>.wav` first.
