import warnings
from importlib.metadata import PackageNotFoundError
from unittest import mock

import pytest

from MLForge.mismatch import _check_version_mismatch


@pytest.mark.parametrize(
    ("MLForge_version", "skinny_version"),
    [
        ("1.0.0", "1.0.0"),
        ("1.0.0.dev0", "1.0.0"),
        ("1.0.0", "1.0.0.dev0"),
        ("1.0.0.dev0", "1.0.0.dev0"),
        ("1.0.0", None),
        (None, "1.0.0"),
        (None, None),
    ],
)
@pytest.mark.parametrize(
    "tracing_version",
    [None, "1.0.0", "1.0.0.dev0"],
)
def test_check_version_mismatch_no_warn(
    MLForge_version: str | None, skinny_version: str | None, tracing_version: str | None
):
    def mock_version(package_name: str) -> str:
        if package_name == "MLForge":
            if MLForge_version is None:
                raise PackageNotFoundError
            return MLForge_version
        elif package_name == "MLForge-skinny":
            if skinny_version is None:
                raise PackageNotFoundError
            return skinny_version
        elif package_name == "MLForge-tracing":
            if tracing_version is None:
                raise PackageNotFoundError
            return tracing_version
        raise ValueError(f"Unexpected package: {package_name}")

    with mock.patch("importlib.metadata.version", side_effect=mock_version) as mv:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            _check_version_mismatch()

        mv.assert_called()


@pytest.mark.parametrize(
    ("MLForge_version", "skinny_version", "tracing_version", "expected"),
    [
        ("1.0.0", "1.0.1", "1.0.0", r"MLForge-skinny \(1.0.1\)"),
        ("1.0.0", "1.0.0", "1.0.1", r"MLForge-tracing \(1.0.1\)"),
        ("1.0.1", "1.0.0", "1.0.0", r"MLForge-skinny \(1.0.0\), MLForge-tracing \(1.0.0\)"),
    ],
)
def test_check_version_mismatch_warn(
    MLForge_version: str,
    skinny_version: str,
    tracing_version: str,
    expected: str,
):
    def mock_version(package_name: str) -> str:
        if package_name == "MLForge":
            return MLForge_version
        elif package_name == "MLForge-skinny":
            return skinny_version
        elif package_name == "MLForge-tracing":
            if tracing_version is None:
                raise PackageNotFoundError
            return tracing_version
        raise ValueError(f"Unexpected package: {package_name}")

    with mock.patch("importlib.metadata.version", side_effect=mock_version) as mv:
        with pytest.warns(
            UserWarning,
            match=rf"Versions of MLForge \([.\w]+\) and child packages {expected} are different",
        ):
            _check_version_mismatch()

        mv.assert_called()
