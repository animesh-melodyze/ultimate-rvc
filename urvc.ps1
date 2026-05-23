# Licensed under the MIT license.
#
# Launcher for the karaoke-vocal-timbre fork of Ultimate RVC (Windows).

<#
.SYNOPSIS

CLI launcher for Ultimate RVC (karaoke vocal-timbre fork).

.DESCRIPTION

Installs dependencies, updates the fork, and exposes the urvc CLI.
This fork is CLI-only — there is no web UI.

.PARAMETER Command
install:   Install dependencies and set up environment.
update:    Git-pull the latest version of this fork.
uninstall: Remove dependencies and generated data.
cli:       Run the urvc CLI (see 'urvc cli --help' for subcommands).
docs:      Generate Typer docs.
uv:        Pass through to uv.
help:      Print help.

.PARAMETER Arguments
Forwarded to the underlying command.

.NOTES
Set $env:URVC_ACCELERATOR to cpu, cuda, or rocm to override the default (cuda).
#>

param (
    [Parameter(Position = 0, HelpMessage="The command to run.")]
    [string]$Command,
    [Parameter(ValueFromRemainingArguments = $true, `
        HelpMessage="The arguments to pass to the command.")]
    [string[]]$Arguments
)

$uvPath = "$(Get-location)\uv"
$venvPath="$uvPath\.venv"
$urvcAccelerator = $env:URVC_ACCELERATOR
if (-not $urvcAccelerator) { $urvcAccelerator = "cuda" }

$env:UV_UNMANAGED_INSTALL = $uvPath
$env:UV_PYTHON_INSTALL_DIR = "$uvPath\python"
$env:UV_PYTHON_BIN_DIR = "$uvPath\python\bin"
$env:VIRTUAL_ENV = $venvPath
$env:UV_PROJECT_ENVIRONMENT = $venvPath
$env:UV_TOOL_DIR = "$uvPath\tools"
$env:UV_TOOL_BIN_DIR = "$uvPath\tools\bin"
$env:PATH = "$uvPath;$env:PATH"

function Main {
    param (
        [string]$Command,
        [string[]]$Arguments
    )

    switch ($Command) {
        "install" {
            Invoke-RestMethod https://astral.sh/uv/0.9.11/install.ps1 | Invoke-Expression
            uv sync --no-editable --extra $urvcAccelerator
            uv run --extra $urvcAccelerator ./src/ultimate_rvc/core/main.py
        }
        "update" {
            git pull
        }
        "uninstall" {
            $confirmationMsg = "Are you sure you want to uninstall?`n" `
                + "This will delete all dependencies and user generated data [Y/n]"
            $confirmation = Read-Host -Prompt $confirmationMsg
            if ($confirmation -in @("", "Y", "y")) {
                git clean -dfX
                Write-Host "Uninstallation complete."
            } else {
                Write-Host "Uninstallation canceled."
            }
        }
        "cli" {
            Assert-Dependencies
            uv run --extra $urvcAccelerator ./src/ultimate_rvc/cli/main.py @Arguments
        }
        "docs" {
            Assert-Dependencies
            if ($Arguments.Length -lt 2) {
                Write-Host "The 'docs' command requires at least two arguments."
                Exit 1
            }
            uv run python -m typer $Arguments[0] utils docs --output $Arguments[1]
        }
        "uv" {
            Assert-Dependencies
            uv @Arguments
        }
        "help" {
            Get-Help $PSCommandPath -Detailed
        }
        default {
            $errorMsg = "Invalid command.`n" `
                + "To see a list of valid commands, use the 'help' command."
            Write-Host $errorMsg
            Exit 1
        }
    }
}

function Assert-Dependencies {
    if (-Not (Test-Path -Path $uvPath)) {
        Write-Host "Dependencies not found. Please run './urvc.ps1 install' first."
        Exit 1
    }
}

Main $Command $Arguments
