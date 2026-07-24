from unittest import mock

import pytest

from MLForge.exceptions import MLForgeException
from MLForge.protos.service_pb2 import Experiment, GetExperiment
from MLForge.store.tracking.rest_store import RestStore
from MLForge.utils.rest_utils import MLForgeHostCreds

ACTIVE_WORKSPACE = "team-a"


def test_supports_workspaces_queries_endpoint():
    creds = MLForgeHostCreds("https://example")
    store = RestStore(lambda: creds)
    response = mock.MagicMock()
    response.status_code = 200
    response.json.return_value = {"workspaces_enabled": True}

    with mock.patch(
        "MLForge.store.workspace_rest_store_mixin.http_request", return_value=response
    ) as mock_http:
        assert store.supports_workspaces is True
        # Cached result prevents additional requests
        assert store.supports_workspaces is True

    mock_http.assert_called_once()
    _, kwargs = mock_http.call_args
    assert kwargs["host_creds"] is creds
    assert kwargs["endpoint"] == "/api/3.0/MLForge/server-info"
    assert kwargs["method"] == "GET"
    assert kwargs["timeout"] == 3
    assert kwargs["max_retries"] == 0
    assert kwargs["raise_on_status"] is False


def test_supports_workspaces_returns_false_on_failure():
    creds = MLForgeHostCreds("https://example")
    store = RestStore(lambda: creds)
    response = mock.MagicMock()
    response.status_code = 404
    response.text = "not found"

    with mock.patch("MLForge.store.workspace_rest_store_mixin.http_request", return_value=response):
        assert store.supports_workspaces is False


def test_supports_workspaces_handles_missing_json_keys():
    creds = MLForgeHostCreds("https://example")
    store = RestStore(lambda: creds)
    response = mock.MagicMock()
    response.status_code = 200
    response.json.return_value = {}

    with mock.patch("MLForge.store.workspace_rest_store_mixin.http_request", return_value=response):
        assert store.supports_workspaces is False


def test_supports_workspaces_returns_false_for_databricks_uri():
    creds = MLForgeHostCreds("databricks")
    store = RestStore(lambda: creds)

    with mock.patch("MLForge.store.workspace_rest_store_mixin.http_request") as mock_http:
        assert store.supports_workspaces is False
        # Should not probe the server for Databricks URIs
        mock_http.assert_not_called()


def test_supports_workspaces_raises_on_server_error():
    creds = MLForgeHostCreds("https://example")
    store = RestStore(lambda: creds)
    response = mock.MagicMock()
    response.status_code = 500
    response.text = "Internal Server Error"

    with mock.patch("MLForge.store.workspace_rest_store_mixin.http_request", return_value=response):
        with pytest.raises(MLForgeException, match="Failed to query.*500"):
            store.supports_workspaces


def test_rest_store_workspace_guard():
    creds = MLForgeHostCreds("https://example")
    store = RestStore(lambda: creds)
    store._workspace_support = False

    with (
        mock.patch(
            "MLForge.store.workspace_rest_store_mixin.get_request_workspace",
            return_value=ACTIVE_WORKSPACE,
        ),
        mock.patch.object(RestStore, "supports_workspaces", property(lambda self: False)),
    ):
        with pytest.raises(
            MLForgeException,
            match="Active workspace 'team-a' cannot be used because the remote server does not",
        ):
            store.search_experiments()


def test_workspace_guard_blocks_log_spans(monkeypatch):
    store = RestStore(lambda: MLForgeHostCreds("https://workspace-host"))
    spans = [mock.MagicMock()]

    monkeypatch.setattr(
        "MLForge.store.workspace_rest_store_mixin.get_request_workspace",
        lambda: ACTIVE_WORKSPACE,
    )
    monkeypatch.setattr(RestStore, "supports_workspaces", property(lambda self: False))

    with pytest.raises(MLForgeException, match="does not support workspaces"):
        store.log_spans("exp-1", spans)


def test_rest_store_get_experiment_has_workspace():
    proto = Experiment(
        experiment_id="1",
        name="test",
        artifact_location="/tmp",
        workspace="other_workspace",
    )
    response = GetExperiment.Response(experiment=proto)

    with mock.patch.object(RestStore, "_call_endpoint", return_value=response) as mock_call:
        store = RestStore(lambda: MLForgeHostCreds("https://hello"))
        result = store.get_experiment("1")

    assert result.workspace == "other_workspace"
    mock_call.assert_called_once()
