import json
import os
from concurrent.futures import ThreadPoolExecutor

import pytest

import MLForge
from MLForge.entities.logged_model_status import LoggedModelStatus
from MLForge.exceptions import MLForgeException
from MLForge.models import Model
from MLForge.tracing.constant import TraceMetadataKey
from MLForge.utils.MLForge_tags import MLForge_MODEL_IS_EXTERNAL


class DummyModel(MLForge.pyfunc.PythonModel):
    def predict(self, model_input):
        return len(model_input) * [0]


class TraceModel(MLForge.pyfunc.PythonModel):
    @MLForge.trace
    def predict(self, model_input):
        return len(model_input) * [0]


def test_model_id_tracking():
    model = TraceModel()
    model.predict([1, 2, 3])
    trace = MLForge.get_trace(MLForge.get_last_active_trace_id())
    assert TraceMetadataKey.MODEL_ID not in trace.info.request_metadata

    with MLForge.start_run():
        info = MLForge.pyfunc.log_model(name="my_model", python_model=model)
        # Log another model to ensure that the model ID is correctly associated with the first model
        MLForge.pyfunc.log_model(name="another_model", python_model=model)

    model = MLForge.pyfunc.load_model(info.model_uri)
    model.predict([4, 5, 6])

    trace = MLForge.get_trace(MLForge.get_last_active_trace_id())
    assert trace is not None
    assert trace.info.request_metadata[TraceMetadataKey.MODEL_ID] == info.model_id


def test_model_id_tracking_evaluate():
    with MLForge.start_run():
        info = MLForge.pyfunc.log_model(name="my_model", python_model=TraceModel())

    MLForge.evaluate(model=info.model_uri, data=[[1, 2, 3]], model_type="regressor", targets=[1])
    trace = MLForge.get_trace(MLForge.get_last_active_trace_id())
    assert trace is not None
    assert trace.info.request_metadata[TraceMetadataKey.MODEL_ID] == info.model_id


def test_model_id_tracking_thread_safety():
    models = []
    for _ in range(5):
        with MLForge.start_run():
            info = MLForge.pyfunc.log_model(
                name="my_model",
                python_model=TraceModel(),
                pip_requirements=[],  # to skip dependency inference
            )
            model = MLForge.pyfunc.load_model(info.model_uri)
            models.append(model)

    def predict(idx, model) -> None:
        model.predict([idx])

    with ThreadPoolExecutor(
        max_workers=len(models), thread_name_prefix="test-logged-models"
    ) as executor:
        futures = [executor.submit(predict, idx, model) for idx, model in enumerate(models)]
        for f in futures:
            f.result()

    traces = MLForge.search_traces(return_type="list")
    assert len(traces) == len(models)
    for trace in traces:
        trace_inputs = trace.info.request_metadata["MLForge.traceInputs"]
        index = json.loads(trace_inputs)["model_input"][0]
        model_id = trace.info.request_metadata["MLForge.modelId"]
        assert model_id == models[index].model_id


def test_run_params_are_logged_to_model():
    with MLForge.start_run():
        MLForge.log_params({"a": 1})
        MLForge.pyfunc.log_model(name="my_model", python_model=DummyModel())

    model = MLForge.last_logged_model()
    assert model.params == {"a": "1"}


def test_run_metrics_are_logged_to_model():
    with MLForge.start_run():
        MLForge.log_metrics({"a": 1, "b": 2})
        MLForge.pyfunc.log_model(name="my_model", python_model=DummyModel())

    model = MLForge.last_logged_model()
    assert [(m.key, m.value) for m in model.metrics] == [("a", 1), ("b", 2)]


def test_log_model_finalizes_existing_pending_model():
    model = MLForge.initialize_logged_model(name="testmodel")
    assert model.status == LoggedModelStatus.PENDING
    MLForge.pyfunc.log_model(python_model=DummyModel(), model_id=model.model_id)
    updated_model = MLForge.get_logged_model(model.model_id)
    assert updated_model.status == LoggedModelStatus.READY


def test_log_model_permits_logging_to_ready_model(tmp_path):
    # Create a non-external model and finalize it to READY status
    model = MLForge.initialize_logged_model(name="testmodel")
    model = MLForge.finalize_logged_model(model.model_id, LoggedModelStatus.READY)
    assert model.status == LoggedModelStatus.READY
    assert model.tags.get(MLForge_MODEL_IS_EXTERNAL, "false").lower() == "false"

    # Verify we can log to the READY model
    MLForge.pyfunc.log_model(python_model=DummyModel(), model_id=model.model_id)

    # Verify the model can be loaded
    MLForge.pyfunc.load_model(f"models:/{model.model_id}")

    # Verify the model artifacts were updated
    dst_dir = os.path.join(tmp_path, "dst")
    MLForge.artifacts.download_artifacts(f"models:/{model.model_id}", dst_path=dst_dir)
    MLForge_model = Model.load(os.path.join(dst_dir, "MLmodel"))
    assert MLForge_model.flavors.get("python_function") is not None


def test_log_model_permits_logging_model_artifacts_to_external_models(tmp_path):
    model = MLForge.create_external_model(name="testmodel")
    assert model.status == LoggedModelStatus.READY
    assert model.tags.get(MLForge_MODEL_IS_EXTERNAL) == "true"
    dst_dir_1 = os.path.join(tmp_path, "dst_1")
    MLForge.artifacts.download_artifacts(f"models:/{model.model_id}", dst_path=dst_dir_1)
    MLForge_model: Model = Model.load(os.path.join(dst_dir_1, "MLmodel"))

    model_info = MLForge.pyfunc.log_model(python_model=DummyModel(), model_id=model.model_id)

    # Verify that the model can now be loaded and is no longer tagged as external
    MLForge.pyfunc.load_model(model_info.model_uri)
    assert MLForge_MODEL_IS_EXTERNAL not in MLForge.get_logged_model(model.model_id).tags
    dst_dir_2 = os.path.join(tmp_path, "dst_2")
    MLForge.artifacts.download_artifacts(f"models:/{model.model_id}", dst_path=dst_dir_2)
    MLForge_model = Model.load(os.path.join(dst_dir_2, "MLmodel"))
    assert MLForge_MODEL_IS_EXTERNAL not in (MLForge_model.metadata or {})


def test_external_logged_model_cannot_be_loaded_with_pyfunc():
    model = MLForge.create_external_model(name="testmodel")
    with pytest.raises(
        MLForgeException,
        match="This model's artifacts are external.*cannot be loaded",
    ):
        MLForge.pyfunc.load_model(f"models:/{model.model_id}")
