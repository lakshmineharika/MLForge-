from unittest import mock

from MLForge.entities import SourceType
from MLForge.tracking.context.databricks_notebook_context import DatabricksNotebookRunContext
from MLForge.utils.MLForge_tags import (
    MLForge_DATABRICKS_NOTEBOOK_ID,
    MLForge_DATABRICKS_NOTEBOOK_PATH,
    MLForge_DATABRICKS_WEBAPP_URL,
    MLForge_DATABRICKS_WORKSPACE_ID,
    MLForge_DATABRICKS_WORKSPACE_URL,
    MLForge_SOURCE_NAME,
    MLForge_SOURCE_TYPE,
)


def test_databricks_notebook_run_context_in_context():
    with mock.patch("MLForge.utils.databricks_utils.is_in_databricks_notebook") as in_notebook_mock:
        assert DatabricksNotebookRunContext().in_context() == in_notebook_mock.return_value


def test_databricks_notebook_run_context_tags():
    patch_notebook_id = mock.patch("MLForge.utils.databricks_utils.get_notebook_id")
    patch_notebook_path = mock.patch("MLForge.utils.databricks_utils.get_notebook_path")
    patch_webapp_url = mock.patch("MLForge.utils.databricks_utils.get_webapp_url")
    patch_workspace_url = mock.patch(
        "MLForge.utils.databricks_utils.get_workspace_url",
        return_value="https://dev.databricks.com",
    )
    patch_workspace_id = mock.patch(
        "MLForge.utils.databricks_utils.get_workspace_id", return_value="123456"
    )
    patch_workspace_url_none = mock.patch(
        "MLForge.utils.databricks_utils.get_workspace_url", return_value=None
    )
    patch_workspace_info = mock.patch(
        "MLForge.utils.databricks_utils.get_workspace_info_from_dbutils",
        return_value=("https://databricks.com", "123456"),
    )

    with (
        patch_notebook_id as notebook_id_mock,
        patch_notebook_path as notebook_path_mock,
        patch_webapp_url as webapp_url_mock,
        patch_workspace_url as workspace_url_mock,
        patch_workspace_info as workspace_info_mock,
        patch_workspace_id as workspace_id_mock,
    ):
        assert DatabricksNotebookRunContext().tags() == {
            MLForge_SOURCE_NAME: notebook_path_mock.return_value,
            MLForge_SOURCE_TYPE: SourceType.to_string(SourceType.NOTEBOOK),
            MLForge_DATABRICKS_NOTEBOOK_ID: notebook_id_mock.return_value,
            MLForge_DATABRICKS_NOTEBOOK_PATH: notebook_path_mock.return_value,
            MLForge_DATABRICKS_WEBAPP_URL: webapp_url_mock.return_value,
            MLForge_DATABRICKS_WORKSPACE_URL: workspace_url_mock.return_value,
            MLForge_DATABRICKS_WORKSPACE_ID: workspace_id_mock.return_value,
        }

    with (
        patch_notebook_id as notebook_id_mock,
        patch_notebook_path as notebook_path_mock,
        patch_webapp_url as webapp_url_mock,
        patch_workspace_url_none as workspace_url_mock,
        patch_workspace_info as workspace_info_mock,
        patch_workspace_id as workspace_id_mock,
    ):
        assert DatabricksNotebookRunContext().tags() == {
            MLForge_SOURCE_NAME: notebook_path_mock.return_value,
            MLForge_SOURCE_TYPE: SourceType.to_string(SourceType.NOTEBOOK),
            MLForge_DATABRICKS_NOTEBOOK_ID: notebook_id_mock.return_value,
            MLForge_DATABRICKS_NOTEBOOK_PATH: notebook_path_mock.return_value,
            MLForge_DATABRICKS_WEBAPP_URL: webapp_url_mock.return_value,
            MLForge_DATABRICKS_WORKSPACE_URL: workspace_info_mock.return_value[0],  # fallback value
            MLForge_DATABRICKS_WORKSPACE_ID: workspace_id_mock.return_value,
        }


def test_databricks_notebook_run_context_tags_nones():
    patch_notebook_id = mock.patch(
        "MLForge.utils.databricks_utils.get_notebook_id", return_value=None
    )
    patch_notebook_path = mock.patch(
        "MLForge.utils.databricks_utils.get_notebook_path", return_value=None
    )
    patch_webapp_url = mock.patch("MLForge.utils.databricks_utils.get_webapp_url", return_value=None)
    patch_workspace_info = mock.patch(
        "MLForge.utils.databricks_utils.get_workspace_info_from_dbutils", return_value=(None, None)
    )

    with patch_notebook_id, patch_notebook_path, patch_webapp_url, patch_workspace_info:
        assert DatabricksNotebookRunContext().tags() == {
            MLForge_SOURCE_NAME: None,
            MLForge_SOURCE_TYPE: SourceType.to_string(SourceType.NOTEBOOK),
        }
