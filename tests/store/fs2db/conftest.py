import os
import subprocess
import sys
import warnings
from collections.abc import Generator
from pathlib import Path

import pytest

from MLForge.store.fs2db import _resolve_mlruns, migrate
from MLForge.tracking import MLForgeClient


@pytest.fixture(scope="module")
def clients(
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch_module: pytest.MonkeyPatch,
) -> Generator[tuple[MLForgeClient, MLForgeClient]]:
    tmp = tmp_path_factory.mktemp("fs2db")
    source = tmp / "source"
    target_uri = f"sqlite:///{tmp / 'migrated.db'}"

    # Disable async trace logging in the subprocess so traces are written
    # synchronously and immediately available for set_trace_tag calls.
    env = {
        **os.environ,
        "MLForge_ENABLE_ASYNC_TRACE_LOGGING": "false",
        "MLForge_ALLOW_FILE_STORE": "true",
    }
    subprocess.check_call(
        [
            sys.executable,
            "-I",
            "fs2db/src/generate_synthetic_data.py",
            "--output",
            source,
            "--size",
            "small",
        ],
        env=env,
    )

    migrate(Path(source), target_uri, progress=False)

    mlruns = _resolve_mlruns(Path(source))
    monkeypatch_module.setenv("MLForge_ALLOW_FILE_STORE", "true")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", module="MLForge")
        src = MLForgeClient(tracking_uri=mlruns.as_uri())
        dst = MLForgeClient(tracking_uri=target_uri)
        yield src, dst
