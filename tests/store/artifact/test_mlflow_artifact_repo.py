import os
import posixpath
import threading
import time
from unittest import mock

import pytest

from MLForge.exceptions import MLForgeException
from MLForge.store.artifact.artifact_repository_registry import get_artifact_repository
from MLForge.store.artifact.MLForge_artifacts_repo import (
    SERVER_INFO_MULTIPART_DOWNLOADS_ENABLED,
    SERVER_INFO_MULTIPART_UPLOADS_ENABLED,
    MLForgeArtifactsRepository,
)
from MLForge.utils.credentials import get_default_host_creds


@pytest.fixture(scope="module", autouse=True)
def set_tracking_uri():
    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.get_tracking_uri",
        return_value="http://localhost:5000/",
    ):
        yield


def test_artifact_uri_factory():
    repo = get_artifact_repository("MLForge-artifacts://test.com")
    assert isinstance(repo, MLForgeArtifactsRepository)


base_url = "/api/2.0/MLForge-artifacts/artifacts"
base_path = "/my/artifact/path"
conditions = [
    (
        f"MLForge-artifacts://myhostname:4242{base_path}/hostport",
        f"http://myhostname:4242{base_url}{base_path}/hostport",
    ),
    (
        f"MLForge-artifacts://myhostname{base_path}/host",
        f"http://myhostname{base_url}{base_path}/host",
    ),
    (
        f"MLForge-artifacts:{base_path}/nohost",
        f"http://localhost:5000{base_url}{base_path}/nohost",
    ),
    (
        f"MLForge-artifacts://{base_path}/redundant",
        f"http://localhost:5000{base_url}{base_path}/redundant",
    ),
    ("MLForge-artifacts:/", f"http://localhost:5000{base_url}"),
]


@pytest.mark.parametrize("tracking_uri", ["http://localhost:5000", "http://localhost:5000/"])
@pytest.mark.parametrize(("artifact_uri", "resolved_uri"), conditions)
def test_MLForge_artifact_uri_formats_resolved(artifact_uri, resolved_uri, tracking_uri):
    assert MLForgeArtifactsRepository.resolve_uri(artifact_uri, tracking_uri) == resolved_uri


def test_MLForge_artifact_uri_raises_with_invalid_tracking_uri():
    with pytest.raises(
        MLForgeException,
        match="When an MLForge-artifacts URI was supplied, the tracking URI must be a valid",
    ):
        MLForgeArtifactsRepository.resolve_uri(
            artifact_uri=f"MLForge-artifacts://myhostname:4242{base_path}/hostport",
            tracking_uri="file:///tmp",
        )


def test_MLForge_artifact_uri_raises_with_invalid_artifact_uri():
    failing_conditions = [f"MLForge-artifacts://5000/{base_path}", "MLForge-artifacts://5000/"]

    for failing_condition in failing_conditions:
        with pytest.raises(
            MLForgeException,
            match="The MLForge-artifacts uri was supplied with a port number: 5000, but no "
            "host was defined.",
        ):
            MLForgeArtifactsRepository(failing_condition)


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("request failed")


class MockStreamResponse(MockResponse):
    def iter_content(self, chunk_size):
        yield self.data.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass


class FileObjectMatcher:
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

    def __eq__(self, other):
        return self.name == other.name and self.mode == other.mode


@pytest.fixture
def MLForge_artifact_repo():
    artifact_uri = "MLForge-artifacts:/api/2.0/MLForge-artifacts/artifacts"
    return MLForgeArtifactsRepository(artifact_uri)


@pytest.fixture
def MLForge_artifact_repo_with_host():
    artifact_uri = "MLForge-artifacts://test.com:5000/api/2.0/MLForge-artifacts/artifacts"
    return MLForgeArtifactsRepository(artifact_uri)


@pytest.mark.parametrize("artifact_path", [None, "dir", "path/to/artifacts/storage"])
def test_log_artifact(MLForge_artifact_repo, tmp_path, artifact_path):
    tmp_path = tmp_path.joinpath("a.txt")
    tmp_path.write_text("0")
    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse({}, 200),
    ) as mock_put:
        MLForge_artifact_repo.log_artifact(tmp_path, artifact_path)
        paths = (artifact_path, tmp_path.name) if artifact_path else (tmp_path.name,)
        mock_put.assert_called_once_with(
            MLForge_artifact_repo._host_creds,
            posixpath.join("/", *paths),
            "PUT",
            extra_headers={"Content-Type": "text/plain"},
            data=FileObjectMatcher(str(tmp_path), "rb"),
        )

    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse({}, 400),
    ):
        with pytest.raises(Exception, match="request failed"):
            MLForge_artifact_repo.log_artifact(tmp_path, artifact_path)


@pytest.mark.parametrize("artifact_path", [None, "dir", "path/to/artifacts/storage"])
def test_log_artifact_with_host_and_port(MLForge_artifact_repo_with_host, tmp_path, artifact_path):
    tmp_path = tmp_path.joinpath("a.txt")
    tmp_path.write_text("0")
    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse({}, 200),
    ) as mock_put:
        MLForge_artifact_repo_with_host.log_artifact(tmp_path, artifact_path)
        paths = (artifact_path, tmp_path.name) if artifact_path else (tmp_path.name,)
        mock_put.assert_called_once_with(
            MLForge_artifact_repo_with_host._host_creds,
            posixpath.join("/", *paths),
            "PUT",
            extra_headers={"Content-Type": "text/plain"},
            data=FileObjectMatcher(str(tmp_path), "rb"),
        )

    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse({}, 400),
    ):
        with pytest.raises(Exception, match="request failed"):
            MLForge_artifact_repo_with_host.log_artifact(tmp_path, artifact_path)


@pytest.mark.parametrize("artifact_path", [None, "dir", "path/to/artifacts/storage"])
def test_log_artifacts(MLForge_artifact_repo, tmp_path, artifact_path):
    tmp_path_a = tmp_path.joinpath("a.txt")
    directory = tmp_path.joinpath("dir")
    directory.mkdir()
    tmp_path_b = directory.joinpath("b.txt")
    tmp_path_a.write_text("0")
    tmp_path_b.write_text("1")

    with mock.patch.object(MLForge_artifact_repo, "log_artifact") as mock_log_artifact:
        MLForge_artifact_repo.log_artifacts(tmp_path, artifact_path)
        mock_log_artifact.assert_has_calls(
            [
                mock.call(str(tmp_path_a), artifact_path),
                mock.call(
                    str(tmp_path_b),
                    posixpath.join(artifact_path, "dir") if artifact_path else "dir",
                ),
            ],
        )

    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse({}, 400),
    ):
        with pytest.raises(Exception, match="request failed"):
            MLForge_artifact_repo.log_artifacts(tmp_path, artifact_path)


def test_list_artifacts(MLForge_artifact_repo):
    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse({}, 200),
    ) as mock_get:
        assert MLForge_artifact_repo.list_artifacts() == []
        endpoint = "/MLForge-artifacts/artifacts"
        url, _ = MLForge_artifact_repo.artifact_uri.split(endpoint, maxsplit=1)
        mock_get.assert_called_once_with(
            get_default_host_creds(url),
            endpoint,
            "GET",
            params={"path": ""},
        )

    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse(
            {
                "files": [
                    {"path": "1.txt", "is_dir": False, "file_size": 1},
                    {"path": "dir", "is_dir": True},
                ]
            },
            200,
        ),
    ):
        assert [a.path for a in MLForge_artifact_repo.list_artifacts()] == ["1.txt", "dir"]

    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse(
            {
                "files": [
                    {"path": "1.txt", "is_dir": False, "file_size": 1},
                    {"path": "dir", "is_dir": True},
                ]
            },
            200,
        ),
    ):
        assert [a.path for a in MLForge_artifact_repo.list_artifacts(path="path")] == [
            "path/1.txt",
            "path/dir",
        ]

    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockResponse({}, 400),
    ):
        with pytest.raises(Exception, match="request failed"):
            MLForge_artifact_repo.list_artifacts()


def read_file(path):
    with open(path) as f:
        return f.read()


@pytest.mark.parametrize("remote_file_path", ["a.txt", "dir/b.xtx"])
def test_download_file(MLForge_artifact_repo, tmp_path, remote_file_path):
    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockStreamResponse("data", 200),
    ) as mock_get:
        tmp_path = tmp_path.joinpath(posixpath.basename(remote_file_path))
        MLForge_artifact_repo._download_file(remote_file_path, tmp_path)
        mock_get.assert_called_once_with(
            MLForge_artifact_repo._host_creds,
            posixpath.join("/", remote_file_path),
            "GET",
            stream=True,
        )
        with open(tmp_path) as f:
            assert f.read() == "data"

    with mock.patch(
        "MLForge.store.artifact.http_artifact_repo.http_request",
        return_value=MockStreamResponse("data", 400),
    ):
        with pytest.raises(Exception, match="request failed"):
            MLForge_artifact_repo._download_file(remote_file_path, tmp_path)


def test_download_artifacts(MLForge_artifact_repo, tmp_path):
    # This test simulates downloading artifacts in the following structure:
    # ---------
    # - a.txt
    # - dir
    #   - b.txt
    # ---------
    def http_request(_host_creds, endpoint, _method, **kwargs):
        # Responses for list_artifacts
        if params := kwargs.get("params"):
            if params.get("path") == "":
                return MockResponse(
                    {
                        "files": [
                            {"path": "a.txt", "is_dir": False, "file_size": 1},
                            {"path": "dir", "is_dir": True},
                        ]
                    },
                    200,
                )
            elif params.get("path") == "dir":
                return MockResponse(
                    {
                        "files": [
                            {"path": "b.txt", "is_dir": False, "file_size": 1},
                        ]
                    },
                    200,
                )
            else:
                Exception("Unreachable")

        # Responses for _download_file
        if endpoint == "/a.txt":
            return MockStreamResponse("data_a", 200)
        elif endpoint == "/dir/b.txt":
            return MockStreamResponse("data_b", 200)
        else:
            raise Exception("Unreachable")

    with mock.patch("MLForge.store.artifact.http_artifact_repo.http_request", http_request):
        MLForge_artifact_repo.download_artifacts("", tmp_path)
        paths = [os.path.join(root, f) for root, _, files in os.walk(tmp_path) for f in files]
        assert [os.path.relpath(p, tmp_path) for p in paths] == [
            "a.txt",
            os.path.join("dir", "b.txt"),
        ]
        assert read_file(paths[0]) == "data_a"
        assert read_file(paths[1]) == "data_b"


def _make_multipart_repo(artifact_uri="MLForge-artifacts:/api/2.0/MLForge-artifacts/artifacts"):
    return MLForgeArtifactsRepository(artifact_uri)


def _mock_server_info_response(uploads=False, downloads=False, status_code=200):
    resp = mock.Mock()
    resp.status_code = status_code
    resp.json.return_value = {
        "store_type": "SqlStore",
        "workspaces_enabled": False,
        "trace_archival_enabled": False,
        SERVER_INFO_MULTIPART_UPLOADS_ENABLED: uploads,
        SERVER_INFO_MULTIPART_DOWNLOADS_ENABLED: downloads,
    }
    return resp


def test_auto_detects_multipart_upload_from_server_info(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    repo = _make_multipart_repo()
    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        return_value=_mock_server_info_response(uploads=True),
    ):
        assert repo._is_multipart_upload_enabled() is True


def test_auto_detects_multipart_download_from_server_info(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_DOWNLOAD", raising=False)
    repo = _make_multipart_repo()
    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        return_value=_mock_server_info_response(downloads=True),
    ):
        assert repo._is_multipart_download_enabled() is True


def test_env_var_true_overrides_server_no_support(monkeypatch):
    monkeypatch.setenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", "true")
    repo = _make_multipart_repo()
    assert repo._is_multipart_upload_enabled() is True


def test_env_var_false_overrides_server_support(monkeypatch):
    monkeypatch.setenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", "false")
    repo = _make_multipart_repo()
    assert repo._is_multipart_upload_enabled() is False


def test_env_var_false_overrides_server_download_support(monkeypatch):
    monkeypatch.setenv("MLForge_ENABLE_PROXY_MULTIPART_DOWNLOAD", "false")
    repo = _make_multipart_repo()
    assert repo._is_multipart_download_enabled() is False


def test_old_server_without_fields_defaults_to_disabled(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_DOWNLOAD", raising=False)
    repo = _make_multipart_repo()

    resp = mock.Mock()
    resp.status_code = 200
    resp.json.return_value = {
        "store_type": "SqlStore",
        "workspaces_enabled": False,
    }

    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        return_value=resp,
    ):
        assert repo._is_multipart_upload_enabled() is False
        assert repo._is_multipart_download_enabled() is False


def test_server_info_404_defaults_to_disabled(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    repo = _make_multipart_repo()

    resp = mock.Mock()
    resp.status_code = 404

    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        return_value=resp,
    ):
        assert repo._is_multipart_upload_enabled() is False


def test_server_info_network_error_defaults_to_disabled(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    repo = _make_multipart_repo()

    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        side_effect=ConnectionError("connection refused"),
    ):
        assert repo._is_multipart_upload_enabled() is False


def test_capabilities_cached_per_instance(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    repo = _make_multipart_repo()

    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        return_value=_mock_server_info_response(uploads=True, downloads=True),
    ) as mock_request:
        assert repo._is_multipart_upload_enabled() is True
        assert repo._is_multipart_download_enabled() is True
        mock_request.assert_called_once()


def test_separate_instances_fetch_independently(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    repo1 = _make_multipart_repo()
    repo2 = _make_multipart_repo()

    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        return_value=_mock_server_info_response(uploads=True),
    ) as mock_request:
        repo1._is_multipart_upload_enabled()
        repo2._is_multipart_upload_enabled()
        assert mock_request.call_count == 2


def test_capability_probe_uses_artifact_host_and_preserves_path_prefix(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.get_tracking_uri",
        return_value="http://tracking.example.com/MLForge",
    ):
        repo = MLForgeArtifactsRepository("MLForge-artifacts://artifacts.example.com:9000/exp")

    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        return_value=_mock_server_info_response(uploads=True),
    ) as mock_request:
        assert repo._is_multipart_upload_enabled() is True

    host_creds = mock_request.call_args.kwargs["host_creds"]
    assert host_creds.host == "http://artifacts.example.com:9000/MLForge"
    assert mock_request.call_args.kwargs["endpoint"] == "/api/3.0/MLForge/server-info"


def test_small_upload_skips_server_info_capability_probe(monkeypatch, tmp_path):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    repo = _make_multipart_repo()
    small_file = tmp_path / "small.bin"
    small_file.write_bytes(b"tiny")

    put_resp = mock.Mock()
    put_resp.status_code = 200

    with (
        mock.patch(
            "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        ) as mock_server_info_request,
        mock.patch(
            "MLForge.store.artifact.http_artifact_repo.http_request",
            return_value=put_resp,
        ),
    ):
        repo.log_artifact(str(small_file))

    mock_server_info_request.assert_not_called()


def test_capabilities_fetch_is_thread_safe(monkeypatch):
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_UPLOAD", raising=False)
    monkeypatch.delenv("MLForge_ENABLE_PROXY_MULTIPART_DOWNLOAD", raising=False)
    repo = _make_multipart_repo()
    results = []

    def slow_server_info(*_args, **_kwargs):
        time.sleep(0.05)
        return _mock_server_info_response(uploads=True, downloads=True)

    with mock.patch(
        "MLForge.store.artifact.MLForge_artifacts_repo.http_request",
        side_effect=slow_server_info,
    ) as mock_request:
        threads = [
            threading.Thread(
                target=lambda: results.append(repo._is_multipart_upload_enabled()),
                name=f"multipart-upload-probe-{idx}",
            )
            for idx in range(4)
        ] + [
            threading.Thread(
                target=lambda: results.append(repo._is_multipart_download_enabled()),
                name=f"multipart-download-probe-{idx}",
            )
            for idx in range(4)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=5)

    assert mock_request.call_count == 1
    assert results == [True] * 8
