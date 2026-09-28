"""Test the Poetry command-line tool."""

import os
import subprocess
import sys
from pathlib import Path


def find_poetry_executable() -> str | None:
    """Find Poetry outside the project environment being inspected."""
    project_scripts = Path(sys.prefix, "Scripts").resolve()
    for path_entry in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path_entry, "poetry.exe")
        if candidate.is_file() and candidate.parent.resolve() != project_scripts:
            return str(candidate)
    return None


def test_poetry_command() -> str:
    """Confirm that Poetry is installed and available on PATH."""
    poetry_executable = find_poetry_executable()
    assert poetry_executable, "The poetry command was not found on PATH."

    result = subprocess.run(
        [poetry_executable, "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    poetry_version = result.stdout.strip()
    assert poetry_version.startswith("Poetry (version"), (
        f"Unexpected Poetry version output: {poetry_version}"
    )
    return poetry_version


def test_project_configuration() -> None:
    """Confirm that Poetry can validate this project's configuration."""
    project_root = Path(__file__).resolve().parent
    poetry_executable = find_poetry_executable()
    assert poetry_executable, "The poetry command was not found on PATH."

    result = subprocess.run(
        [poetry_executable, "check"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "Poetry rejected the project configuration:\n"
        f"{result.stdout}{result.stderr}"
    )


def main() -> None:
    poetry_version = test_poetry_command()
    test_project_configuration()

    print(f"Poetry executable test passed: {poetry_version}")
    print("Poetry project configuration test passed.")


if __name__ == "__main__":
    main()
