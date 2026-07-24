import subprocess
import sys
from pathlib import Path

import pytest

from MLForge.utils.os import is_windows


@pytest.mark.skipif(is_windows(), reason="This test fails on Windows")
def test_import_MLForge(tmp_path: Path):
    tmp_script = tmp_path.joinpath("test.py")
    tmp_script.write_text(
        """
from pathlib import Path

import MLForge

# Ensure importing MLForge does not create an mlruns directory
assert not Path("mlruns").exists()
"""
    )
    python_ver = ".".join(map(str, sys.version_info[:2]))
    repo_root = Path(__file__).resolve().parent.parent
    subprocess.check_call(
        [
            "uv",
            "run",
            f"--with={repo_root}",
            f"--directory={tmp_path}",
            f"--python={python_ver}",
            "python",
            tmp_script.name,
        ],
    )
