import os
import subprocess
from pathlib import Path
from unittest import mock

import pytest
import requests

import MLForge
from MLForge import MLForgeClient, register_model
from MLForge.entities.model_registry import ModelVersion, RegisteredModel
from MLForge.exceptions import MLForgeException
from MLForge.protos.databricks_pb2 import (
    ALREADY_EXISTS,
    INTERNAL_ERROR,
    RESOURCE_ALREADY_EXISTS,
    RESOURCE_DOES_NOT_EXIST,
)
from MLForge.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS
from MLForge.utils.databricks_utils import DatabricksRuntimeVersion
from MLForge.utils.env_pack import EnvPackConfig


def test_register_model_with_runs_uri():
    class TestModel(MLForge.pyfunc.PythonModel):
        def predict(self, model_input):
            return model_input

    with MLForge.start_run() as run:
        MLForge.pyfunc.log_model(name="model", python_model=TestModel())

    register_model(f"runs:/{run.info.run_id}/model", "Model 1")
    mv = MLForgeClient().get_model_version("Model 1", "1")
    assert mv.name == "Model 1"


def test_register_model_with_non_runs_uri():
    create_model_patch = mock.patch.object(
        MLForgeClient, "create_registered_model", return_value=RegisteredModel("Model 1")
    )
    create_version_patch = mock.patch.object(
        MLForgeClient,
        "_create_model_version",
        return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
    )
    with create_model_patch, create_version_patch:
        register_model("s3:/some/path/to/model", "Model 1")
        MLForgeClient.create_registered_model.assert_called_once_with("Model 1")
        MLForgeClient._create_model_version.assert_called_once_with(
            name="Model 1",
            run_id=None,
            tags=None,
            source="s3:/some/path/to/model",
            await_creation_for=DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
            local_model_path=None,
            model_id=None,
        )


@pytest.mark.parametrize("error_code", [RESOURCE_ALREADY_EXISTS, ALREADY_EXISTS])
def test_register_model_with_existing_registered_model(error_code):
    create_model_patch = mock.patch.object(
        MLForgeClient,
        "create_registered_model",
        side_effect=MLForgeException("Some Message", error_code),
    )
    create_version_patch = mock.patch.object(
        MLForgeClient,
        "_create_model_version",
        return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
    )
    with create_model_patch, create_version_patch:
        register_model("s3:/some/path/to/model", "Model 1")
        MLForgeClient.create_registered_model.assert_called_once_with("Model 1")
        MLForgeClient._create_model_version.assert_called_once_with(
            name="Model 1",
            run_id=None,
            source="s3:/some/path/to/model",
            tags=None,
            await_creation_for=DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
            local_model_path=None,
            model_id=None,
        )


def test_register_model_with_unexpected_MLForge_exception_in_create_registered_model():
    with mock.patch.object(
        MLForgeClient,
        "create_registered_model",
        side_effect=MLForgeException("Dunno", INTERNAL_ERROR),
    ) as mock_create_registered_model:
        with pytest.raises(MLForgeException, match="Dunno"):
            register_model("s3:/some/path/to/model", "Model 1")
        mock_create_registered_model.assert_called_once_with("Model 1")


def test_register_model_with_unexpected_exception_in_create_registered_model():
    with mock.patch.object(
        MLForgeClient, "create_registered_model", side_effect=Exception("Dunno")
    ) as create_registered_model_mock:
        with pytest.raises(Exception, match="Dunno"):
            register_model("s3:/some/path/to/model", "Model 1")
        create_registered_model_mock.assert_called_once_with("Model 1")


def test_register_model_with_tags():
    tags = {"a": "1"}

    class TestModel(MLForge.pyfunc.PythonModel):
        def predict(self, model_input):
            return model_input

    with MLForge.start_run() as run:
        MLForge.pyfunc.log_model(name="model", python_model=TestModel())

    register_model(f"runs:/{run.info.run_id}/model", "Model 1", tags=tags)
    mv = MLForgeClient().get_model_version("Model 1", "1")
    assert mv.tags == tags


def test_register_model_prints_uc_model_version_url(monkeypatch):
    orig_registry_uri = MLForge.get_registry_uri()
    MLForge.set_registry_uri("databricks-uc")
    workspace_id = "123"
    model_id = "m-123"
    name = "name.MLForge.test_model"
    version = "1"
    with (
        mock.patch("MLForge.tracking._model_registry.fluent.eprint") as mock_eprint,
        mock.patch(
            "MLForge.tracking._model_registry.fluent.get_workspace_url",
            return_value="https://databricks.com",
        ) as mock_url,
        mock.patch(
            "MLForge.tracking._model_registry.fluent.get_workspace_id",
            return_value=workspace_id,
        ) as mock_workspace_id,
        mock.patch(
            "MLForge.MLForgeClient.create_registered_model",
            return_value=RegisteredModel(name),
        ) as mock_create_model,
        mock.patch(
            "MLForge.MLForgeClient._create_model_version",
            return_value=ModelVersion(name, version, creation_timestamp=123),
        ) as mock_create_version,
        mock.patch(
            "MLForge.MLForgeClient.get_logged_model",
            return_value=mock.Mock(model_id=model_id, name=name, tags={}),
        ) as mock_get_logged_model,
        mock.patch("MLForge.MLForgeClient.set_logged_model_tags") as mock_set_logged_model_tags,
    ):
        register_model(f"models:/{model_id}", name)
        expected_url = (
            "https://databricks.com/explore/data/models/name/MLForge/test_model/version/1?o=123"
        )
        mock_eprint.assert_called_with(
            f"🔗 Created version '{version}' of model '{name}': {expected_url}"
        )
        mock_url.assert_called_once()
        mock_workspace_id.assert_called_once()
        mock_create_model.assert_called_once()
        mock_create_version.assert_called_once()
        mock_get_logged_model.assert_called_once()
        mock_set_logged_model_tags.assert_called_once()

        # Test that the URL is not printed when the environment variable is set to false
        mock_eprint.reset_mock()
        monkeypatch.setenv("MLForge_PRINT_MODEL_URLS_ON_CREATION", "false")
        register_model(f"models:/{model_id}", name)
        mock_eprint.assert_called_with("Created version '1' of model 'name.MLForge.test_model'.")

    # Clean up the global variables set by the server
    MLForge.set_registry_uri(orig_registry_uri)


def test_register_model_skips_logged_model_tag_when_not_found(monkeypatch):
    # When the source logged model doesn't exist (e.g., cross-workspace copy),
    # register_model should succeed and log a warning instead of raising.
    orig_registry_uri = MLForge.get_registry_uri()
    MLForge.set_registry_uri("databricks-uc")
    model_id = "m-cross-ws"
    name = "name.MLForge.cross_ws_model"
    version = "1"
    with (
        mock.patch("MLForge.tracking._model_registry.fluent.eprint"),
        mock.patch("MLForge.tracking._model_registry.fluent.get_workspace_url", return_value=None),
        mock.patch(
            "MLForge.MLForgeClient.create_registered_model",
            return_value=RegisteredModel(name),
        ),
        mock.patch(
            "MLForge.MLForgeClient._create_model_version",
            return_value=ModelVersion(name, version, creation_timestamp=123),
        ),
        mock.patch(
            "MLForge.MLForgeClient.get_logged_model",
            side_effect=MLForgeException("not found", error_code=RESOURCE_DOES_NOT_EXIST),
        ) as mock_get_logged_model,
        mock.patch("MLForge.MLForgeClient.set_logged_model_tags") as mock_set_tags,
    ):
        # Should not raise even though get_logged_model fails
        mv = register_model(f"models:/{model_id}", name)
        assert mv.version == version
        mock_get_logged_model.assert_called_once()
        mock_set_tags.assert_not_called()

    MLForge.set_registry_uri(orig_registry_uri)


def test_set_model_version_tag():
    class TestModel(MLForge.pyfunc.PythonModel):
        def predict(self, model_input):
            return model_input

    MLForge.pyfunc.log_model(name="model", python_model=TestModel(), registered_model_name="Model 1")

    mv = MLForgeClient().get_model_version("Model 1", "1")
    assert mv.tags == {}
    MLForge.set_model_version_tag(
        name="Model 1",
        version=1,
        key="key",
        value="value",
    )
    mv = MLForgeClient().get_model_version("Model 1", "1")
    assert mv.tags == {"key": "value"}


def test_register_model_with_2_x_model(tmp_path: Path):
    tracking_uri = f"sqlite:///{tmp_path / 'MLForge.db'}"
    artifact_location = (tmp_path / "artifacts").as_uri()

    code = """
import sys
import MLForge

assert MLForge.__version__.startswith("2."), MLForge.__version__

tracking_uri, artifact_location, out = sys.argv[1:]
MLForge.set_tracking_uri(tracking_uri)
exp_id = MLForge.create_experiment("test", artifact_location=artifact_location)
MLForge.set_experiment(experiment_id=exp_id)

with MLForge.start_run() as run:
    model_info = MLForge.pyfunc.log_model(
        python_model=lambda *args: None,
        artifact_path="model",
        # When `python_model` is a function, either `input_example` or `pip_requirements`
        # must be provided.
        pip_requirements=["MLForge"],
    )
    assert model_info.model_uri.startswith("runs:/")
    with open(out, "w") as f:
        f.write(model_info.model_uri)
"""
    out = tmp_path / "output.txt"
    # Log a model using MLForge 2.x (let 2.x create the DB)
    subprocess.check_call(
        [
            "uv",
            "run",
            "--isolated",
            "--no-project",
            "--with",
            "MLForge<3",
            "python",
            "-I",
            "-c",
            code,
            tracking_uri,
            artifact_location,
            out,
        ],
        env=os.environ.copy() | {"UV_INDEX_STRATEGY": "unsafe-first-match"},
    )
    # Register the model with MLForge 3.x (migration happens automatically)
    MLForge.set_tracking_uri(tracking_uri)
    model_uri = out.read_text().strip()
    MLForge.register_model(model_uri, "model")


@pytest.fixture
def mock_dbr_version():
    """Mock DatabricksRuntimeVersion to simulate a supported client image."""
    with mock.patch(
        "MLForge.utils.databricks_utils.DatabricksRuntimeVersion.parse",
        return_value=DatabricksRuntimeVersion(
            is_client_image=True,
            major=2,  # Supported version
            minor=0,
            is_gpu_image=False,
        ),
    ):
        yield


def test_register_model_with_env_pack(tmp_path, mock_dbr_version):
    # Mock download_artifacts to return a path
    mock_artifacts_dir = tmp_path / "artifacts"
    mock_artifacts_dir.mkdir()
    (mock_artifacts_dir / "requirements.txt").write_text("numpy==1.21.0")

    with (
        mock.patch(
            "MLForge.utils.env_pack.download_artifacts",
            return_value=str(mock_artifacts_dir),
        ),
        mock.patch("subprocess.run", return_value=mock.Mock(returncode=0)),
        mock.patch(
            "MLForge.tracking._model_registry.fluent.pack_env_for_databricks_model_serving"
        ) as mock_pack_env,
        mock.patch(
            "MLForge.tracking._model_registry.fluent.stage_model_for_databricks_model_serving"
        ) as mock_stage_model,
        mock.patch(
            "MLForge.MLForgeClient._create_model_version",
            return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
        ) as mock_create_version,
        mock.patch(
            "MLForge.MLForgeClient.get_model_version",
            return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
        ),
    ):
        # Set up the mock pack_env to yield a path
        mock_pack_env.return_value.__enter__.return_value = str(mock_artifacts_dir)

        # Call register_model with env_pack
        register_model("models:/test-model/1", "Model 1", env_pack="databricks_model_serving")

        # Verify pack_env was called with correct arguments
        mock_pack_env.assert_called_once_with(
            "models:/test-model/1",
            enforce_pip_requirements=True,
            local_model_path=None,
        )

        # Verify _create_model_version was called with packed artifacts path
        mock_create_version.assert_called_once_with(
            name="Model 1",
            source="models:/test-model/1",
            run_id=None,
            tags=None,
            await_creation_for=DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
            local_model_path=str(mock_artifacts_dir),
            model_id=None,
        )

        # Verify stage_model was called with correct arguments
        mock_stage_model.assert_called_once_with(
            model_name="Model 1",
            model_version="1",
        )


@pytest.mark.parametrize("install_deps", [True, False])
def test_register_model_with_env_pack_config(tmp_path, install_deps):
    # Mock download_artifacts to return a path
    mock_artifacts_dir = tmp_path / "artifacts"
    mock_artifacts_dir.mkdir()
    (mock_artifacts_dir / "requirements.txt").write_text("numpy==1.21.0")

    with (
        mock.patch(
            "MLForge.utils.env_pack.download_artifacts",
            return_value=str(mock_artifacts_dir),
        ),
        mock.patch("subprocess.run", return_value=mock.Mock(returncode=0)),
        mock.patch(
            "MLForge.tracking._model_registry.fluent.pack_env_for_databricks_model_serving"
        ) as mock_pack_env,
        mock.patch(
            "MLForge.tracking._model_registry.fluent.stage_model_for_databricks_model_serving"
        ) as mock_stage_model,
        mock.patch(
            "MLForge.MLForgeClient._create_model_version",
            return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
        ) as mock_create_version,
        mock.patch(
            "MLForge.MLForgeClient.get_model_version",
            return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
        ),
    ):
        # Set up the mock pack_env to yield a path
        mock_pack_env.return_value.__enter__.return_value = str(mock_artifacts_dir)

        # Call register_model with env_pack
        register_model(
            "models:/test-model/1",
            "Model 1",
            env_pack=EnvPackConfig(
                name="databricks_model_serving", install_dependencies=install_deps
            ),
        )

        mock_pack_env.assert_called_once_with(
            "models:/test-model/1",
            enforce_pip_requirements=install_deps,
            local_model_path=None,
        )

        # Verify _create_model_version was called with packed artifacts path
        mock_create_version.assert_called_once_with(
            name="Model 1",
            source="models:/test-model/1",
            run_id=None,
            tags=None,
            await_creation_for=DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
            local_model_path=str(mock_artifacts_dir),
            model_id=None,
        )

        mock_stage_model.assert_called_once_with(
            model_name="Model 1",
            model_version="1",
        )


def test_register_model_with_env_pack_staging_failure(tmp_path, mock_dbr_version):
    # Mock download_artifacts to return a path
    mock_artifacts_dir = tmp_path / "artifacts"
    mock_artifacts_dir.mkdir()
    (mock_artifacts_dir / "requirements.txt").write_text("numpy==1.21.0")

    with (
        mock.patch(
            "MLForge.utils.env_pack.download_artifacts",
            return_value=str(mock_artifacts_dir),
        ),
        mock.patch("subprocess.run", return_value=mock.Mock(returncode=0)),
        mock.patch(
            "MLForge.tracking._model_registry.fluent.pack_env_for_databricks_model_serving"
        ) as mock_pack_env,
        mock.patch(
            "MLForge.tracking._model_registry.fluent.stage_model_for_databricks_model_serving",
            side_effect=requests.exceptions.HTTPError("Staging failed"),
        ) as mock_stage_model,
        mock.patch(
            "MLForge.MLForgeClient._create_model_version",
            return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
        ) as mock_create_version,
        mock.patch(
            "MLForge.MLForgeClient.get_model_version",
            return_value=ModelVersion("Model 1", "1", creation_timestamp=123),
        ),
        mock.patch("MLForge.tracking._model_registry.fluent.eprint") as mock_eprint,
    ):
        # Set up the mock pack_env to yield a path
        mock_pack_env.return_value.__enter__.return_value = str(mock_artifacts_dir)

        # Call register_model with env_pack
        register_model("models:/test-model/1", "Model 1", env_pack="databricks_model_serving")

        # Verify pack_env was called with correct arguments
        mock_pack_env.assert_called_once_with(
            "models:/test-model/1",
            enforce_pip_requirements=True,
            local_model_path=None,
        )

        # Verify _create_model_version was called with packed artifacts path
        mock_create_version.assert_called_once_with(
            name="Model 1",
            source="models:/test-model/1",
            run_id=None,
            tags=None,
            await_creation_for=DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
            local_model_path=str(mock_artifacts_dir),
            model_id=None,
        )

        # Verify stage_model was called with correct arguments
        mock_stage_model.assert_called_once_with(
            model_name="Model 1",
            model_version="1",
        )

        # Verify warning message was printed
        mock_eprint.assert_any_call(
            "Failed to stage model for Databricks Model Serving: Staging failed. "
            "The model was registered successfully and is available for serving, but may take "
            "longer to deploy."
        )
