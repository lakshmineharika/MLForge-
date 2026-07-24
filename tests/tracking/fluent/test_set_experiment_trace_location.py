from unittest import mock

import pytest

import MLForge
from MLForge.entities import Experiment
from MLForge.entities.experiment_tag import ExperimentTag
from MLForge.entities.trace_location import UnityCatalog
from MLForge.exceptions import MLForgeException
from MLForge.tracking._uc_upsell import show_existing_experiment_upsell, show_new_experiment_upsell
from MLForge.tracking.fluent import (
    _resolve_experiment_to_trace_location,
    _sync_trace_destination_and_provider,
)
from MLForge.utils.MLForge_tags import (
    MLForge_EXPERIMENT_DATABRICKS_TRACE_ANNOTATIONS_TABLE,
    MLForge_EXPERIMENT_DATABRICKS_TRACE_DESTINATION_PATH,
    MLForge_EXPERIMENT_DATABRICKS_TRACE_LOG_STORAGE_TABLE,
    MLForge_EXPERIMENT_DATABRICKS_TRACE_SPAN_STORAGE_TABLE,
)


def _experiment(tags=None):
    tag_entities = [ExperimentTag(k, v) for k, v in (tags or {}).items()]
    return Experiment(
        experiment_id="123",
        name="test-experiment",
        artifact_location="file:/tmp",
        lifecycle_stage="active",
        tags=tag_entities,
    )


def test_invalid_type_raises():
    with pytest.raises(MLForgeException, match="UnityCatalog"):
        _resolve_experiment_to_trace_location(
            experiment=_experiment(),
            trace_location="not-a-location",
        )


def test_uc_schema_location_is_rejected():
    from MLForge.entities.trace_location import UCSchemaLocation

    with pytest.raises(MLForgeException, match="UnityCatalog"):
        _resolve_experiment_to_trace_location(
            experiment=_experiment(),
            trace_location=UCSchemaLocation("catalog", "schema"),
        )


def test_no_trace_location_returns_none():
    result = _resolve_experiment_to_trace_location(
        experiment=_experiment(),
        trace_location=None,
    )
    assert result is None


def test_non_databricks_backend_raises():
    with (
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="file:///tmp"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=False),
    ):
        with pytest.raises(MLForgeException, match="only supported with a Databricks tracking URI"):
            _resolve_experiment_to_trace_location(
                experiment=_experiment(),
                trace_location=UnityCatalog("catalog", "schema", "prefix"),
            )


def test_set_experiment_with_table_prefix_env_var_points_to_trace_location_param(monkeypatch):
    from MLForge.tracing.provider import _get_tracer

    monkeypatch.setenv("MLForge_TRACING_DESTINATION", "catalog.schema.prefix")

    MLForge.tracing.reset()
    MLForge.set_experiment("test-experiment")

    # The error surfaces lazily at trace creation time (provider init),
    # not eagerly at set_experiment time.
    with pytest.raises(
        MLForgeException,
        match=r"Unity Catalog table-prefix destinations "
        r"\(<catalog_name>\.<schema_name>\.<table_prefix>\) are not supported in "
        r"MLForge_TRACING_DESTINATION.*Use `MLForge\.set_experiment",
    ):
        _get_tracer("test")

    MLForge.tracing.reset()


def test_set_experiment_defaults_empty_prefix_to_experiment_id():
    resolved = UnityCatalog("catalog", "schema", table_prefix="123")

    with (
        mock.patch("MLForge.tracking.fluent.TrackingServiceClient") as mock_client_cls,
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            return_value=resolved,
        ) as mock_resolve,
        mock.patch("MLForge.tracking.fluent._sync_trace_destination_and_provider"),
    ):
        client = mock_client_cls.return_value
        client.get_experiment_by_name.return_value = _experiment()  # experiment_id="123"

        original = UnityCatalog("catalog", "schema")  # no prefix
        MLForge.set_experiment("test-experiment", trace_location=original)

        # Verify _resolve was called with a location that has the experiment ID as prefix
        _, kwargs = mock_resolve.call_args
        passed_location = kwargs["trace_location"]
        assert passed_location.table_prefix == "123"
        assert passed_location.catalog_name == "catalog"
        assert passed_location.schema_name == "schema"

        # Original object should not be mutated
        assert original.table_prefix is None


def test_creates_and_links_when_no_existing_location(monkeypatch):
    monkeypatch.setenv("MLForge_TRACING_SQL_WAREHOUSE_ID", "warehouse-1")
    requested = UnityCatalog("catalog", "schema", table_prefix="prefix")
    resolved = UnityCatalog("catalog", "schema", table_prefix="prefix")

    with (
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="databricks"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=True),
        mock.patch("MLForge.tracing.client.TracingClient") as tc_cls,
    ):
        tc = tc_cls.return_value
        tc._create_or_get_trace_location.return_value = resolved

        result = _resolve_experiment_to_trace_location(
            experiment=_experiment(),
            trace_location=requested,
        )

        assert result is resolved
        tc._create_or_get_trace_location.assert_called_once_with(requested, "warehouse-1")
        tc._link_trace_location.assert_called_once_with(
            experiment_id="123",
            location=resolved,
        )


def test_noop_when_existing_location_matches():
    requested = UnityCatalog("catalog", "schema", table_prefix="prefix")
    experiment = _experiment(
        tags={
            MLForge_EXPERIMENT_DATABRICKS_TRACE_DESTINATION_PATH: "catalog.schema.prefix",
            MLForge_EXPERIMENT_DATABRICKS_TRACE_SPAN_STORAGE_TABLE: (
                "catalog.schema.prefix_otel_spans"
            ),
            MLForge_EXPERIMENT_DATABRICKS_TRACE_LOG_STORAGE_TABLE: (
                "catalog.schema.prefix_otel_logs"
            ),
            MLForge_EXPERIMENT_DATABRICKS_TRACE_ANNOTATIONS_TABLE: (
                "catalog.schema.prefix_annotations"
            ),
        }
    )

    with (
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="databricks"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=True),
    ):
        result = _resolve_experiment_to_trace_location(
            experiment=experiment,
            trace_location=requested,
        )

        assert result == requested
        assert result._otel_spans_table_name == "catalog.schema.prefix_otel_spans"
        assert result._otel_logs_table_name == "catalog.schema.prefix_otel_logs"
        assert result._annotations_table_name == "catalog.schema.prefix_annotations"


def test_errors_when_existing_location_differs():
    requested = UnityCatalog("catalog", "schema", table_prefix="new_prefix")
    experiment = _experiment(
        tags={MLForge_EXPERIMENT_DATABRICKS_TRACE_DESTINATION_PATH: "catalog.schema.old_prefix"}
    )

    with (
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="databricks"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=True),
    ):
        with pytest.raises(MLForgeException, match="already linked to a different"):
            _resolve_experiment_to_trace_location(
                experiment=experiment,
                trace_location=requested,
            )


def test_existing_uc_schema_destination_rejects_table_prefix():
    requested = UnityCatalog("catalog", "schema", table_prefix="pfx")
    experiment = _experiment(
        tags={MLForge_EXPERIMENT_DATABRICKS_TRACE_DESTINATION_PATH: "catalog.schema"}
    )

    with (
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="databricks"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=True),
    ):
        with pytest.raises(MLForgeException, match="already linked to a different"):
            _resolve_experiment_to_trace_location(
                experiment=experiment,
                trace_location=requested,
            )


def test_link_failure_on_new_experiment_includes_retry_guidance():
    with (
        mock.patch("MLForge.tracking.fluent.TrackingServiceClient") as mock_client_cls,
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            side_effect=MLForgeException("backend error"),
        ) as mock_resolve,
    ):
        client = mock_client_cls.return_value
        # Simulate: experiment_name lookup returns None (not found) -> create -> get
        client.get_experiment_by_name.return_value = None
        client.create_experiment.return_value = "456"
        new_exp = _experiment()
        client.get_experiment.return_value = new_exp

        with pytest.raises(
            MLForgeException, match="fix the issue and call set_experiment again"
        ) as exc_info:
            MLForge.set_experiment(
                "new-exp",
                trace_location=UnityCatalog("cat", "sch", "pfx"),
            )

        assert "backend error" in exc_info.value.message
        mock_resolve.assert_called_once()


def test_link_failure_on_existing_experiment_reraises_original():
    with (
        mock.patch("MLForge.tracking.fluent.TrackingServiceClient") as mock_client_cls,
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            side_effect=MLForgeException("backend error"),
        ) as mock_resolve,
    ):
        client = mock_client_cls.return_value
        # Simulate: experiment already exists
        client.get_experiment_by_name.return_value = _experiment()

        with pytest.raises(MLForgeException, match="backend error"):
            MLForge.set_experiment(
                "test-experiment",
                trace_location=UnityCatalog("cat", "sch", "pfx"),
            )

        mock_resolve.assert_called_once()


def test_set_experiment_wires_trace_location_to_returned_experiment():
    resolved = UnityCatalog("catalog", "schema", table_prefix="pfx")

    with (
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            return_value=resolved,
        ) as mock_register,
        mock.patch(
            "MLForge.tracking.fluent._sync_trace_destination_and_provider",
        ) as mock_sync,
    ):
        experiment = MLForge.set_experiment("test-trace-loc-integration")

    mock_register.assert_called_once()
    _, kwargs = mock_register.call_args
    assert kwargs["experiment"].name == "test-trace-loc-integration"
    mock_sync.assert_called_once_with(resolved)
    assert experiment.trace_location is resolved


def test_set_experiment_with_trace_location_installs_uc_processor():
    from MLForge.tracing.export.uc_table import DatabricksUCTableSpanExporter
    from MLForge.tracing.processor.uc_table import DatabricksUCTableSpanProcessor
    from MLForge.tracing.provider import _MLForge_TRACE_USER_DESTINATION, _get_tracer

    resolved = UnityCatalog("catalog", "schema", table_prefix="pfx")
    MLForge.tracing.reset()
    _MLForge_TRACE_USER_DESTINATION.reset()

    with (
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            return_value=resolved,
        ) as mock_register,
    ):
        experiment = MLForge.set_experiment("test-uc-processor")

    mock_register.assert_called_once()
    assert experiment.trace_location is resolved

    tracer = _get_tracer("test")
    processors = tracer.span_processor._span_processors
    assert len(processors) == 1
    assert isinstance(processors[0], DatabricksUCTableSpanProcessor)
    assert isinstance(processors[0].span_exporter, DatabricksUCTableSpanExporter)

    _MLForge_TRACE_USER_DESTINATION.reset()
    MLForge.tracing.reset()


def test_set_experiment_without_trace_location_does_not_install_uc_processor():
    from MLForge.tracing.processor.uc_table import DatabricksUCTableSpanProcessor
    from MLForge.tracing.provider import _MLForge_TRACE_USER_DESTINATION, _get_tracer

    MLForge.tracing.reset()
    _MLForge_TRACE_USER_DESTINATION.reset()

    MLForge.set_experiment("test-no-uc-processor")

    tracer = _get_tracer("test")
    processors = tracer.span_processor._span_processors
    assert all(not isinstance(p, DatabricksUCTableSpanProcessor) for p in processors)

    _MLForge_TRACE_USER_DESTINATION.reset()
    MLForge.tracing.reset()


@pytest.fixture
def _clean_tracing_state():
    from MLForge.tracing.provider import _MLForge_TRACE_USER_DESTINATION, provider

    _MLForge_TRACE_USER_DESTINATION.reset()
    provider.reset()
    yield _MLForge_TRACE_USER_DESTINATION, provider
    _MLForge_TRACE_USER_DESTINATION.reset()
    provider.reset()


def test_sync_fresh_session_with_uc_location_sets_destination_only(_clean_tracing_state):
    destination_registry, _ = _clean_tracing_state
    location = UnityCatalog("catalog", "schema", table_prefix="pfx")

    _sync_trace_destination_and_provider(location)

    assert destination_registry.get() is location


def test_sync_experiment_switch_with_uc_location_resets_and_sets_new(_clean_tracing_state):
    destination_registry, prov = _clean_tracing_state
    destination_registry.set(UnityCatalog("catalog", "schema", table_prefix="old"))
    prov.once._done = True

    new_location = UnityCatalog("catalog", "schema", table_prefix="new")
    _sync_trace_destination_and_provider(new_location)

    assert destination_registry.get() is new_location
    assert not prov.once._done


def test_sync_experiment_switch_without_location_clears_and_resets(_clean_tracing_state):
    destination_registry, prov = _clean_tracing_state
    destination_registry.set(UnityCatalog("catalog", "schema", table_prefix="old"))
    prov.once._done = True

    _sync_trace_destination_and_provider(None)

    assert destination_registry.get() is None
    assert not prov.once._done


def test_sync_fresh_session_without_location_is_noop(_clean_tracing_state):
    destination_registry, prov = _clean_tracing_state

    _sync_trace_destination_and_provider(None)

    assert destination_registry.get() is None
    assert not prov.once._done


def test_show_uc_upsell_message_existing_experiment():
    with mock.patch("MLForge.tracking._uc_upsell.eprint") as mock_eprint:
        show_existing_experiment_upsell()
        mock_eprint.assert_called_once_with(
            "\033[1;38;5;208mIf you are using MLForge Tracing, you can migrate your traces "
            "to Unity Catalog for unlimited storage, fine-grained access controls, "
            "and queryability from notebooks, SQL, and dashboards. "
            "\033[94mLearn more: https://docs.databricks.com/aws/en/MLForge3/genai/tracing/migrate-traces-to-uc\033[0m"
        )


def test_show_uc_upsell_message_new_experiment():
    with mock.patch("MLForge.tracking._uc_upsell.eprint") as mock_eprint:
        show_new_experiment_upsell()
        mock_eprint.assert_called_once_with(
            "\033[1;38;5;208mIf you are using MLForge Tracing, consider storing your "
            "traces in Unity Catalog for unlimited storage (no 100,000 trace limit), "
            "fine-grained access controls, and queryability from notebooks, SQL, "
            "and dashboards. \033[94mLearn more: "
            "https://docs.databricks.com/aws/en/MLForge3/genai/tracing/trace-unity-catalog"
            "\033[0m"
        )


def test_uc_upsell_existing_shown_for_existing_non_uc_experiment_on_databricks():
    exp = _experiment()
    with (
        mock.patch("MLForge.tracking.fluent.TrackingServiceClient") as mock_client_cls,
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            return_value=None,
        ),
        mock.patch("MLForge.tracking.fluent._sync_trace_destination_and_provider"),
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="databricks"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=True),
        mock.patch("MLForge.tracking._uc_upsell.eprint") as mock_eprint,
    ):
        mock_client_cls.return_value.get_experiment_by_name.return_value = exp
        MLForge.set_experiment("test-experiment")
        mock_eprint.assert_called_once_with(
            "\033[1;38;5;208mIf you are using MLForge Tracing, you can migrate your traces "
            "to Unity Catalog for unlimited storage, fine-grained access controls, "
            "and queryability from notebooks, SQL, and dashboards. "
            "\033[94mLearn more: https://docs.databricks.com/aws/en/MLForge3/genai/tracing/migrate-traces-to-uc\033[0m"
        )


def test_uc_upsell_new_shown_for_newly_created_experiment_on_databricks():
    exp = _experiment()
    with (
        mock.patch("MLForge.tracking.fluent.TrackingServiceClient") as mock_client_cls,
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            return_value=None,
        ),
        mock.patch("MLForge.tracking.fluent._sync_trace_destination_and_provider"),
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="databricks"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=True),
        mock.patch("MLForge.tracking._uc_upsell.eprint") as mock_eprint,
    ):
        client = mock_client_cls.return_value
        client.get_experiment_by_name.return_value = None
        client.create_experiment.return_value = "123"
        client.get_experiment.return_value = exp
        MLForge.set_experiment("test-experiment")
        mock_eprint.assert_called_once()
        message = mock_eprint.call_args[0][0]
        assert "If you are using MLForge Tracing" in message
        assert "consider storing your traces in Unity Catalog" in message


def test_uc_upsell_not_shown_when_experiment_has_uc_tag():
    exp = _experiment(
        tags={MLForge_EXPERIMENT_DATABRICKS_TRACE_DESTINATION_PATH: "catalog.schema.prefix"}
    )
    with (
        mock.patch("MLForge.tracking.fluent.TrackingServiceClient") as mock_client_cls,
        mock.patch(
            "MLForge.tracking.fluent._resolve_experiment_to_trace_location",
            return_value=None,
        ),
        mock.patch("MLForge.tracking.fluent._sync_trace_destination_and_provider"),
        mock.patch("MLForge.tracking.fluent._resolve_tracking_uri", return_value="databricks"),
        mock.patch("MLForge.tracking.fluent.is_databricks_uri", return_value=True),
        mock.patch("MLForge.tracking._uc_upsell.eprint") as mock_eprint,
    ):
        mock_client_cls.return_value.get_experiment_by_name.return_value = exp
        MLForge.set_experiment("test-experiment")
        mock_eprint.assert_not_called()
