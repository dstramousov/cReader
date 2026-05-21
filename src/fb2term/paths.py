"""Filesystem path helpers."""

from __future__ import annotations

import os
from pathlib import Path


APP_DIR_NAME = "fb2term"


def get_data_dir() -> Path:
    """Return the application data directory.

    Returns:
        XDG-compatible application data directory.
    """

    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home).expanduser() / APP_DIR_NAME
    return Path.home() / ".local" / "share" / APP_DIR_NAME


def get_state_path() -> Path:
    """Return the default reader state file path.

    Returns:
        Path to the JSON state file.
    """

    return get_data_dir() / "state.json"
