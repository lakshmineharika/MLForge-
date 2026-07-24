from unittest import mock

import pytest

from MLForge.tracing.utils.environment import resolve_env_metadata
from MLForge.utils.MLForge_tags import (
    MLForge_DATABRICKS_NOTEBOOK_ID,
    MLForge_DATABRICKS_NOTEBOOK_PATH,
    MLForge_GIT_BRANCH,
    MLForge_GIT_COMMIT,
    MLForge_GIT_REPO_URL,
    MLForge_SOURCE_NAME,
    MLForge_SOURCE_TYPE,
    MLForge_USER,
)
from MLForge.version import IS_TRACING_SDK_ONLY


@pytest.fixture(autouse=True)
def clear_lru_cache():
    resolve_env_metadata.cache_clear()


def test_resolve_env_metadata():
    expected_metadata = {
        MLForge_USER: mock.ANY,
        MLForge_SOURCE_NAME: mock.ANY,
        MLForge_SOURCE_TYPE: "LOCAL",
    }
    if not IS_TRACING_SDK_ONLY:
        expected_metadata.update({
            MLForge_GIT_BRANCH: mock.ANY,
            MLForge_GIT_COMMIT: mock.ANY,
            MLForge_GIT_REPO_URL: mock.ANY,
        })
    assert resolve_env_metadata() == expected_metadata


def test_resolve_env_metadata_in_databricks_notebook():
    with (
        mock.patch(
            "MLForge.tracking.context.databricks_notebook_context.databricks_utils"
        ) as mock_db_utils,
        mock.patch("MLForge.tracing.utils.environment.is_in_databricks_notebook", return_value=True),
    ):
        mock_db_utils.is_in_databricks_notebook.return_value = True
        mock_db_utils.get_notebook_id.return_value = "notebook_123"
        mock_db_utils.get_notebook_path.return_value = "/Users/bob/test.py"
        mock_db_utils.get_webapp_url.return_value = None
        mock_db_utils.get_workspace_url.return_value = None
        mock_db_utils.get_workspace_id.return_value = None
        mock_db_utils.get_workspace_info_from_dbutils.return_value = (None, None)

        assert resolve_env_metadata() == {
            MLForge_USER: mock.ANY,
            MLForge_SOURCE_NAME: "/Users/bob/test.py",
            MLForge_SOURCE_TYPE: "NOTEBOOK",
            MLForge_DATABRICKS_NOTEBOOK_ID: "notebook_123",
            MLForge_DATABRICKS_NOTEBOOK_PATH: "/Users/bob/test.py",
        }
