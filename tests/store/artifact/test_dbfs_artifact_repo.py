from unittest import mock

import pytest

from MLForge.exceptions import MLForgeException
from MLForge.store.artifact.databricks_run_artifact_repo import DatabricksRunArtifactRepository
from MLForge.store.artifact.dbfs_artifact_repo import (
    DbfsRestArtifactRepository,
    dbfs_artifact_repo_factory,
)
from MLForge.store.artifact.local_artifact_repo import LocalArtifactRepository


@pytest.mark.parametrize(
    ("artifact_uri", "uri_at_init"),
    [("dbfs:/path", "file:///dbfs/path"), ("dbfs://databricks/path", "file:///dbfs/path")],
)
def test_dbfs_artifact_repo_factory_local_repo(artifact_uri, uri_at_init):
    with (
        mock.patch("MLForge.utils.databricks_utils.is_dbfs_fuse_available", return_value=True),
        mock.patch(
            "MLForge.store.artifact.dbfs_artifact_repo.LocalArtifactRepository", autospec=True
        ) as mock_repo,
    ):
        repo = dbfs_artifact_repo_factory(artifact_uri)
        assert isinstance(repo, LocalArtifactRepository)
        mock_repo.assert_called_once_with(uri_at_init, tracking_uri=None, registry_uri=None)


@pytest.mark.parametrize(
    "artifact_uri",
    [
        "dbfs://someProfile@databricks/path",
        "dbfs://somewhere:else@databricks/path",
        # Model registry paths should use the REST artifact repo, both when communicating
        # with the current workspace (authority component = "databricks") and other workspaces
        # (authority component = "someProfile@databricks"), as model registry paths cannot
        # be accessed via the local filesystem (via FUSE)
        "dbfs://databricks/databricks/MLForge-registry/abcdefg123/path",
        "dbfs://someProfile@databricks/MLForge-registry/abcdefg123/path",
        "dbfs://somewhere:else@databricks/MLForge-registry/abcdefg123/path",
        "dbfs:/databricks/MLForge-registry/abcdefg123/path",
    ],
)
def test_dbfs_artifact_repo_factory_dbfs_rest_repo(artifact_uri):
    with (
        mock.patch("MLForge.utils.databricks_utils.is_dbfs_fuse_available", return_value=True),
        mock.patch(
            "MLForge.store.artifact.dbfs_artifact_repo.DbfsRestArtifactRepository", autospec=True
        ) as mock_repo,
    ):
        repo = dbfs_artifact_repo_factory(artifact_uri)
        assert isinstance(repo, DbfsRestArtifactRepository)
        mock_repo.assert_called_once_with(artifact_uri, tracking_uri=None, registry_uri=None)


@pytest.mark.parametrize(
    "artifact_uri",
    [
        ("dbfs:/databricks/MLForge-tracking/experiment/1/run/2"),
        ("dbfs://@databricks/databricks/MLForge-tracking/experiment/1/run/2"),
        ("dbfs://someProfile@databricks/databricks/MLForge-tracking/experiment/1/run/2"),
    ],
)
def test_dbfs_artifact_repo_factory_acled_paths(artifact_uri):
    with (
        mock.patch(
            "MLForge.store.artifact.dbfs_artifact_repo.DatabricksRunArtifactRepository",
            autospec=True,
        ) as mock_repo,
    ):
        repo = dbfs_artifact_repo_factory(artifact_uri)
        assert isinstance(repo, DatabricksRunArtifactRepository)
        mock_repo.assert_called_once_with(artifact_uri, tracking_uri=None, registry_uri=None)


@pytest.mark.parametrize(
    "artifact_uri", [("notdbfs:/path"), ("dbfs://some:where@notdatabricks/path")]
)
def test_dbfs_artifact_repo_factory_errors(artifact_uri):
    with pytest.raises(MLForgeException, match="DBFS URI must be of the form dbfs"):
        dbfs_artifact_repo_factory(artifact_uri)
