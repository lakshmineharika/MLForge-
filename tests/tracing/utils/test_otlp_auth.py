import base64
from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import patch

from MLForge.tracing.utils.otlp import MLForge_EXPERIMENT_ID_HEADER, build_otlp_headers
from MLForge.utils.credentials import MLForgeCreds


@contextmanager
def mock_creds(username: str | None = None, password: str | None = None) -> Generator[None]:
    with patch(
        "MLForge.tracing.utils.otlp.read_MLForge_creds",
        return_value=MLForgeCreds(username=username, password=password),
    ) as m:
        yield
    m.assert_called_once()


def test_build_otlp_headers_no_credentials(monkeypatch):
    monkeypatch.delenv("MLForge_TRACKING_TOKEN", raising=False)
    with mock_creds():
        headers = build_otlp_headers("42")
    assert headers == {MLForge_EXPERIMENT_ID_HEADER: "42"}
    assert "Authorization" not in headers


def test_build_otlp_headers_basic_auth(monkeypatch):
    monkeypatch.delenv("MLForge_TRACKING_TOKEN", raising=False)
    with mock_creds(username="admin", password="s3cret"):
        headers = build_otlp_headers("7")
    expected = base64.standard_b64encode(b"admin:s3cret").decode()
    assert headers[MLForge_EXPERIMENT_ID_HEADER] == "7"
    assert headers["Authorization"] == f"Basic {expected}"


def test_build_otlp_headers_bearer_token(monkeypatch):
    monkeypatch.setenv("MLForge_TRACKING_TOKEN", "tok-abc")
    with mock_creds():
        headers = build_otlp_headers("1")
    assert headers[MLForge_EXPERIMENT_ID_HEADER] == "1"
    assert headers["Authorization"] == "Bearer tok-abc"


def test_build_otlp_headers_basic_auth_takes_precedence_over_token(monkeypatch):
    monkeypatch.setenv("MLForge_TRACKING_TOKEN", "tok-xyz")
    with mock_creds(username="admin", password="pass"):
        headers = build_otlp_headers("5")
    expected = base64.standard_b64encode(b"admin:pass").decode()
    assert headers[MLForge_EXPERIMENT_ID_HEADER] == "5"
    assert headers["Authorization"] == f"Basic {expected}"
