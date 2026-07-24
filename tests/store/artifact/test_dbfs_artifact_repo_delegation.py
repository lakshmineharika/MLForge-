import os
from unittest import mock

import pytest

from MLForge.store.artifact.artifact_repository_registry import get_artifact_repository
from MLForge.store.artifact.databricks_run_artifact_repo import DatabricksRunArtifactRepository
from MLForge.store.artifact.dbfs_artifact_repo import DbfsRestArtifactRepository
from MLForge.store.artifact.local_artifact_repo import LocalArtifactRepository
from MLForge.utils.rest_utils import MLForgeHostCreds


@pytest.fixture(autouse=True)
def set_fake_databricks_creds(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://localhost:8080")
    monkeypatch.setenv("DATABRICKS_TOKEN", "token")


@pytest.fixture
def host_creds_mock():
    with mock.patch(
        "MLForge.store.artifact.dbfs_artifact_repo._get_host_creds_from_default_store",
        return_value=lambda: MLForgeHostCreds("http://host"),
    ):
        yield


def test_dbfs_artifact_repo_delegates_to_correct_repo(host_creds_mock, monkeypatch):
    with mock.patch("MLForge.utils.databricks_utils.is_dbfs_fuse_available", return_value=True):
        # fuse available
        artifact_uri = "dbfs:/databricks/my/absolute/dbfs/path"
        repo = get_artifact_repository(artifact_uri)
        assert isinstance(repo, LocalArtifactRepository)
        assert repo.artifact_dir == os.path.join(
            os.path.sep, "dbfs", "databricks", "my", "absolute", "dbfs", "path"
        )
        # fuse available but a model repository DBFS location
        repo = get_artifact_repository("dbfs:/databricks/MLForge-registry/version12345/models")
        assert isinstance(repo, DbfsRestArtifactRepository)
        # fuse not available
        with monkeypatch.context() as m:
            m.setenv("MLForge_ENABLE_DBFS_FUSE_ARTIFACT_REPO", "false")
            fuse_disabled_repo = get_artifact_repository(artifact_uri)
        assert isinstance(fuse_disabled_repo, DbfsRestArtifactRepository)
        assert fuse_disabled_repo.artifact_uri == artifact_uri

    with mock.patch("MLForge.utils.databricks_utils.is_dbfs_fuse_available", return_value=False):
        rest_repo = get_artifact_repository(artifact_uri)
        assert isinstance(rest_repo, DbfsRestArtifactRepository)
        assert rest_repo.artifact_uri == artifact_uri

        mock_uri = "dbfs:/databricks/MLForge-tracking/MOCK-EXP/MOCK-RUN-ID/artifacts"
        databricks_repo = get_artifact_repository(mock_uri)
        assert isinstance(databricks_repo, DatabricksRunArtifactRepository)
        assert databricks_repo.artifact_uri == mock_uri
