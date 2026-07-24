import contextlib
import inspect
import sys
from io import StringIO
from typing import Any, NamedTuple
from unittest import mock

import anthropic
import autogen
import boto3
import dspy
import google.genai
import groq
import keras
import langchain
import lightgbm
import lightning
import litellm
import llama_index.core
import mistralai
import openai
import pyspark
import pyspark.ml
import pytest
import pytorch_lightning
import sklearn
import statsmodels
import tensorflow
import transformers
import xgboost

import MLForge
from MLForge.ml_package_versions import FLAVOR_TO_MODULE_NAME
from MLForge.utils.autologging_utils import (
    AutologgingEventLogger,
    autologging_is_disabled,
    get_autologging_config,
)

from tests.autologging.fixtures import (
    reset_stderr,  # noqa: F401
    test_mode_off,
    test_mode_on,
)
from tests.helper_functions import start_mock_openai_server

library_to_MLForge_module_without_spark_datasource = {
    tensorflow: MLForge.tensorflow,
    keras: MLForge.keras,
    sklearn: MLForge.sklearn,
    xgboost: MLForge.xgboost,
    lightgbm: MLForge.lightgbm,
    statsmodels: MLForge.statsmodels,
    pyspark.ml: MLForge.pyspark.ml,
    pytorch_lightning: MLForge.pytorch,
    lightning: MLForge.pytorch,
    transformers: MLForge.transformers,
}

try:
    import setfit

    library_to_MLForge_module_without_spark_datasource[setfit] = MLForge.transformers
except ImportError:
    pass

library_to_MLForge_module_genai = {
    openai: MLForge.openai,
    llama_index.core: MLForge.llama_index,
    langchain: MLForge.langchain,
    anthropic: MLForge.anthropic,
    dspy: MLForge.dspy,
    litellm: MLForge.litellm,
    google.genai: MLForge.gemini,
    boto3: MLForge.bedrock,
    groq: MLForge.groq,
    mistralai: MLForge.mistral,
    autogen: MLForge.ag2,
    # TODO: once Python 3.10 is introduced, enable smolagents
    # smolagents: MLForge.smolagents,
}

library_to_MLForge_module_traditional_ai = {
    **library_to_MLForge_module_without_spark_datasource,
    pyspark: MLForge.spark,
}

library_to_MLForge_module = {
    **library_to_MLForge_module_traditional_ai,
    **library_to_MLForge_module_genai,
}


@pytest.fixture(autouse=True)
def reset_global_states():
    from MLForge.utils.autologging_utils import AUTOLOGGING_INTEGRATIONS

    for value in AUTOLOGGING_INTEGRATIONS.values():
        value.clear()

    for integration_name in library_to_MLForge_module:
        try:
            del MLForge.utils.import_hooks._post_import_hooks[integration_name.__name__]
        except Exception:
            pass

    # setfit may not be in library_to_MLForge_module when incompatible with transformers 5.x
    MLForge.utils.import_hooks._post_import_hooks.pop("setfit", None)

    assert all(v == {} for v in AUTOLOGGING_INTEGRATIONS.values())
    assert MLForge.utils.import_hooks._post_import_hooks == {}

    yield

    for value in AUTOLOGGING_INTEGRATIONS.values():
        value.clear()

    for integration_name in library_to_MLForge_module:
        try:
            del MLForge.utils.import_hooks._post_import_hooks[integration_name.__name__]
        except Exception:
            pass

    # TODO: Remove these when we run ci with Python >= 3.10
    MLForge.utils.import_hooks._post_import_hooks.pop("smolagents", None)
    MLForge.utils.import_hooks._post_import_hooks.pop("pydantic_ai", None)
    MLForge.utils.import_hooks._post_import_hooks.pop("crewai", None)
    MLForge.utils.import_hooks._post_import_hooks.pop("autogen_agentchat", None)
    MLForge.utils.import_hooks._post_import_hooks.pop("semantic_kernel", None)
    MLForge.utils.import_hooks._post_import_hooks.pop("agno", None)
    MLForge.utils.import_hooks._post_import_hooks.pop("strands", None)
    MLForge.utils.import_hooks._post_import_hooks.pop("haystack", None)
    # setfit may not be in library_to_MLForge_module when incompatible with transformers 5.x
    MLForge.utils.import_hooks._post_import_hooks.pop("setfit", None)
    # TODO: Remove this line when we stop supporting google.generativeai
    MLForge.utils.import_hooks._post_import_hooks.pop("google.generativeai", None)

    assert all(v == {} for v in AUTOLOGGING_INTEGRATIONS.values())
    assert MLForge.utils.import_hooks._post_import_hooks == {}


# We are pretending the module is not already imported (in reality it is, at the top of this file),
#   and is only imported when we call wrapt.notify_module_loaded in the tests below. Normally,
#   notify_module_loaded would be called by register_post_import_hook if it sees that the module
#   is already loaded.
def only_register(callback_fn, module, overwrite):
    MLForge.utils.import_hooks._post_import_hooks[module] = [callback_fn]


@pytest.fixture(autouse=True)
def disable_new_import_hook_firing_if_module_already_exists(request):
    if "do_not_disable_new_import_hook_firing_if_module_already_exists" in request.keywords:
        yield
    else:
        with mock.patch("MLForge.tracking.fluent.register_post_import_hook", wraps=only_register):
            yield


@pytest.mark.usefixtures(test_mode_off.__name__)
@pytest.mark.parametrize(("library", "MLForge_module"), library_to_MLForge_module.items())
def test_universal_autolog_does_not_throw_if_specific_autolog_throws_in_standard_mode(
    library, MLForge_module
):
    # In this file mock is conflicting with lazy loading. Call the module to avoid errors.
    # TODO(chenmoneygithub): investigate why this is happening and remove the call.
    MLForge_module.autolog
    with mock.patch(MLForge_module.__name__ + ".autolog") as autolog_mock:
        autolog_mock.side_effect = Exception("asdf")
        MLForge.autolog()
        if library not in (pyspark, pyspark.ml):
            autolog_mock.assert_not_called()

        MLForge.utils.import_hooks.notify_module_loaded(library)
        autolog_mock.assert_called_once()


@pytest.mark.usefixtures(test_mode_on.__name__)
@pytest.mark.parametrize(("library", "MLForge_module"), library_to_MLForge_module.items())
def test_universal_autolog_throws_if_specific_autolog_throws_in_test_mode(library, MLForge_module):
    with mock.patch(MLForge_module.__name__ + ".autolog") as autolog_mock:
        autolog_mock.side_effect = Exception("asdf")

        MLForge.autolog()
        with pytest.raises(Exception, match="asdf"):
            MLForge.utils.import_hooks.notify_module_loaded(library)

        autolog_mock.assert_called_once()


@pytest.mark.parametrize(("library", "MLForge_module"), library_to_MLForge_module.items())
def test_universal_autolog_calls_specific_autologs_correctly(library, MLForge_module):
    integrations_with_additional_config = [xgboost, lightgbm, sklearn]
    args_to_test = {
        "log_models": False,
        "log_datasets": False,
        "log_traces": False,
        "disable": True,
        "exclusive": True,
        "disable_for_unsupported_versions": True,
        "silent": True,
    }
    if library in integrations_with_additional_config:
        args_to_test.update({"log_input_examples": True, "log_model_signatures": True})

    MLForge.autolog(**args_to_test)

    MLForge.utils.import_hooks.notify_module_loaded(library)
    params_to_check = set(inspect.signature(MLForge_module.autolog).parameters) & set(args_to_test)

    for arg_key in params_to_check:
        assert (
            get_autologging_config(MLForge_module.autolog.integration_name, arg_key, None)
            == args_to_test[arg_key]
        )


@pytest.mark.parametrize("is_databricks", [False, True])
@pytest.mark.parametrize("disable", [False, True])
def test_genai_auto_logging(is_databricks, disable):
    with mock.patch("MLForge.tracking.fluent.is_in_databricks_runtime", return_value=is_databricks):
        MLForge.autolog(disable=disable)

    for library, MLForge_module in library_to_MLForge_module_traditional_ai.items():
        MLForge.utils.import_hooks.notify_module_loaded(library)
        assert get_autologging_config(MLForge_module.autolog.integration_name, "disable") == disable

    # Auto logging for GenAI libraries should be disabled when disable=False on Databricks
    expected = None if is_databricks and (not disable) else disable
    for library, MLForge_module in library_to_MLForge_module_genai.items():
        MLForge.utils.import_hooks.notify_module_loaded(library)
        assert get_autologging_config(MLForge_module.autolog.integration_name, "disable") == expected


def test_universal_autolog_calls_pyspark_immediately_in_databricks():
    with mock.patch("MLForge.tracking.fluent.is_in_databricks_runtime", return_value=True):
        MLForge.autolog()
        assert not autologging_is_disabled(MLForge.spark.FLAVOR_NAME)

        MLForge.autolog(disable=True)
        assert autologging_is_disabled(MLForge.spark.FLAVOR_NAME)

        MLForge.autolog(disable=False)
        assert not autologging_is_disabled(MLForge.spark.FLAVOR_NAME)

        with mock.patch("MLForge.spark.autolog", wraps=MLForge.spark.autolog) as autolog_mock:
            # there should be no import hook on pyspark since autologging was already
            # applied to an active spark session
            MLForge.utils.import_hooks.notify_module_loaded(pyspark)
            autolog_mock.assert_not_called()


@pytest.mark.parametrize("config", [{"disable": False}, {"disable": True}])
def test_universal_autolog_attaches_pyspark_import_hook_in_non_databricks(config):
    with mock.patch(
        "MLForge.spark.autolog", wraps=MLForge.spark.autolog, autospec=True
    ) as autolog_mock:
        autolog_mock.integration_name = "spark"

        MLForge.autolog(**config)
        autolog_mock.assert_not_called()

        MLForge.utils.import_hooks.notify_module_loaded(pyspark)

        # assert autolog is called once pyspark is imported
        autolog_mock.assert_called_once_with(**config, silent=False)


def test_universal_autolog_makes_expected_event_logging_calls():
    class TestLogger(AutologgingEventLogger):
        class LoggerCall(NamedTuple):
            integration: Any
            call_args: Any
            call_kwargs: Any

        def __init__(self):
            self.calls = []

        def reset(self):
            self.calls = []

        def log_autolog_called(self, integration, call_args, call_kwargs):
            self.calls.append(TestLogger.LoggerCall(integration, call_args, call_kwargs))

    logger = TestLogger()
    AutologgingEventLogger.set_logger(logger)

    MLForge.autolog(exclusive=True, disable=True)

    universal_autolog_event_logging_calls = [
        call for call in logger.calls if call.integration == "MLForge"
    ]
    assert len(universal_autolog_event_logging_calls) == 1
    call = universal_autolog_event_logging_calls[0]
    assert call.integration == "MLForge"
    assert {"disable": True, "exclusive": True}.items() <= call.call_kwargs.items()


def test_autolog_obeys_disabled():
    from MLForge.utils.autologging_utils import AUTOLOGGING_INTEGRATIONS

    MLForge.autolog(disable=True)
    MLForge.utils.import_hooks.notify_module_loaded(sklearn)
    assert get_autologging_config("sklearn", "disable")

    MLForge.autolog()
    MLForge.utils.import_hooks.notify_module_loaded(sklearn)
    MLForge.autolog(disable=True)
    MLForge.utils.import_hooks.notify_module_loaded(sklearn)
    assert get_autologging_config("sklearn", "disable")

    MLForge.autolog(disable=False)
    MLForge.utils.import_hooks.notify_module_loaded(sklearn)
    assert not get_autologging_config("sklearn", "disable")
    MLForge.sklearn.autolog(disable=True)
    assert get_autologging_config("sklearn", "disable")

    AUTOLOGGING_INTEGRATIONS.clear()
    MLForge.autolog(disable_for_unsupported_versions=False)
    MLForge.utils.import_hooks.notify_module_loaded(sklearn)
    assert not get_autologging_config("sklearn", "disable_for_unsupported_versions")
    MLForge.autolog(disable_for_unsupported_versions=True)
    MLForge.utils.import_hooks.notify_module_loaded(sklearn)
    assert get_autologging_config("sklearn", "disable_for_unsupported_versions")

    MLForge.sklearn.autolog(disable_for_unsupported_versions=False)
    assert not get_autologging_config("sklearn", "disable_for_unsupported_versions")
    MLForge.sklearn.autolog(disable_for_unsupported_versions=True)
    assert get_autologging_config("sklearn", "disable_for_unsupported_versions")


def test_autolog_success_message_obeys_disabled():
    with mock.patch("MLForge.tracking.fluent._logger.info") as autolog_logger_mock:
        MLForge.autolog(disable=True)
        MLForge.utils.import_hooks.notify_module_loaded(sklearn)
        autolog_logger_mock.assert_not_called()

        MLForge.autolog()
        MLForge.utils.import_hooks.notify_module_loaded(sklearn)
        autolog_logger_mock.assert_called()

        autolog_logger_mock.reset_mock()

        MLForge.autolog(disable=False)
        MLForge.utils.import_hooks.notify_module_loaded(sklearn)
        autolog_logger_mock.assert_called()


# Currently some GenAI integrations do not fully follow standard autolog annotation
@pytest.mark.parametrize("library", library_to_MLForge_module_traditional_ai.keys())
@pytest.mark.parametrize("disable", [False, True])
@pytest.mark.parametrize("exclusive", [False, True])
@pytest.mark.parametrize("disable_for_unsupported_versions", [False, True])
@pytest.mark.parametrize("log_models", [False, True])
@pytest.mark.parametrize("log_datasets", [False, True])
@pytest.mark.parametrize("log_input_examples", [False, True])
@pytest.mark.parametrize("log_model_signatures", [False, True])
def test_autolog_obeys_silent_mode(
    library,
    disable,
    exclusive,
    disable_for_unsupported_versions,
    log_models,
    log_datasets,
    log_input_examples,
    log_model_signatures,
):
    stream = StringIO()
    sys.stderr = stream

    MLForge.autolog(
        silent=True,
        disable=disable,
        exclusive=exclusive,
        disable_for_unsupported_versions=disable_for_unsupported_versions,
        log_models=log_models,
        log_datasets=log_datasets,
        log_input_examples=log_input_examples,
        log_model_signatures=log_model_signatures,
    )

    MLForge.utils.import_hooks.notify_module_loaded(library)

    assert not stream.getvalue()


@pytest.mark.do_not_disable_new_import_hook_firing_if_module_already_exists
def test_last_active_run_retrieves_autologged_run():
    from sklearn.ensemble import RandomForestRegressor

    MLForge.autolog()
    rf = RandomForestRegressor(n_estimators=1, max_depth=1, max_features=1)
    rf.fit([[1, 2]], [[3]])
    rf.predict([[2, 1]])

    autolog_run = MLForge.last_active_run()
    assert autolog_run is not None
    assert autolog_run.info.run_id is not None


@pytest.mark.do_not_disable_new_import_hook_firing_if_module_already_exists
def test_extra_tags_MLForge_autolog():
    from sklearn.ensemble import RandomForestRegressor

    from MLForge.exceptions import MLForgeException
    from MLForge.utils.MLForge_tags import MLForge_AUTOLOGGING

    MLForge.autolog(extra_tags={"test_tag": "autolog", MLForge_AUTOLOGGING: "123"})
    rf = RandomForestRegressor(n_estimators=1, max_depth=1, max_features=1)
    rf.fit([[1, 2]], [[3]])
    autolog_run = MLForge.last_active_run()
    assert autolog_run.data.tags["test_tag"] == "autolog"
    assert autolog_run.data.tags[MLForge_AUTOLOGGING] == "sklearn"

    with pytest.raises(MLForgeException, match="Invalid `extra_tags` type"):
        MLForge.autolog(extra_tags="test_tag")


@pytest.mark.parametrize(("library", "MLForge_module"), library_to_MLForge_module.items())
def test_autolog_excluded_flavors(library, MLForge_module):
    MLForge.autolog(exclude_flavors=[MLForge_module.__name__.removeprefix("MLForge.")])
    MLForge.utils.import_hooks.notify_module_loaded(library)

    assert get_autologging_config(MLForge_module.autolog.integration_name, "disable") is None


# Tests for auto tracing
@pytest.fixture
def mock_openai(monkeypatch):
    with start_mock_openai_server() as base_url:
        monkeypatch.setenv("OPENAI_API_KEY", "test")
        monkeypatch.setenv("OPENAI_API_BASE", base_url)
        yield base_url


@pytest.fixture(params=[True, False])
def other_library_present(request):
    if request.param:
        yield
    else:
        with mock.patch.dict(sys.modules, {"openai": openai}):
            yield


@pytest.mark.parametrize("is_databricks", [False, True])
@pytest.mark.parametrize("disable", [False, True])
def test_autolog_genai_auto_tracing(mock_openai, is_databricks, disable, other_library_present):
    with mock.patch("MLForge.tracking.fluent.is_in_databricks_runtime", return_value=is_databricks):
        MLForge.autolog(disable=disable)
    MLForge.utils.import_hooks.notify_module_loaded(openai)
    client = openai.OpenAI(api_key="test", base_url=mock_openai)
    client.completions.create(
        prompt="test",
        model="gpt-4o-mini",
        temperature=0,
    )

    # GenAI should not be enabled by MLForge.autolog even if disable=False on Databricks
    if is_databricks or disable:
        trace = MLForge.get_trace(MLForge.get_last_active_trace_id(), flush=True)
        assert trace is None
    else:
        trace = MLForge.get_trace(MLForge.get_last_active_trace_id(), flush=True)
        assert trace is not None
        assert trace.info.status == "OK"
        assert len(trace.data.spans) == 1
        span = trace.data.spans[0]
        assert span.inputs == {"prompt": "test", "model": "gpt-4o-mini", "temperature": 0}
        assert span.outputs["id"] == "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7"


@contextlib.contextmanager
def reset_module_import():
    """
    Temporarily reset the module import state to simulate the module being not imported.
    """
    original_modules = {}
    for module_name in FLAVOR_TO_MODULE_NAME.values():
        original_modules[module_name] = sys.modules.get(module_name)

    try:
        yield
    finally:
        for module_name, original_module in original_modules.items():
            if original_module is not None:
                sys.modules[module_name] = original_module


@pytest.mark.parametrize("flavor_and_module", FLAVOR_TO_MODULE_NAME.items())
@pytest.mark.parametrize("disable", [False, True])
@pytest.mark.do_not_disable_new_import_hook_firing_if_module_already_exists
def test_autolog_genai_import(disable, flavor_and_module):
    flavor, module = flavor_and_module

    # pytorch-lightning is not valid flavor name.
    # paddle autologging is not in the list of autologging integrations.
    # crewai, smolagents, and semantic_kernel require Python 3.10+ (our CI runs on Python 3.9).
    if flavor in {
        "pytorch-lightning",
        "paddle",
        "crewai",
        "smolagents",
        "pydantic_ai",
        "autogen",
        "semantic_kernel",
        "agno",
        "strands",
        "haystack",
    }:
        return

    with reset_module_import():
        MLForge.autolog(disable=disable)

        __import__(module)

        assert get_autologging_config(flavor, "disable") == disable
