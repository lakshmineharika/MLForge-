import pytest
from opentelemetry import trace as otel_trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

import MLForge
from MLForge.entities.span import SpanStatusCode, encode_span_id
from MLForge.entities.trace_location import MLForgeExperimentLocation
from MLForge.entities.trace_state import TraceState
from MLForge.environment_variables import (
    MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT,
    MLForge_USE_DEFAULT_TRACER_PROVIDER,
)
from MLForge.tracing.processor.MLForge_v3 import MLForgeV3SpanProcessor
from MLForge.tracing.provider import get_bridged_tracer_provider, provider, set_destination
from MLForge.utils.os import is_windows

from tests.tracing.helper import get_traces


@pytest.fixture(autouse=True)
def reset_tracing():
    yield
    # Explicitly reset all tracing state to ensure test isolation when tests
    # switch between MLForge_USE_DEFAULT_TRACER_PROVIDER modes. This is needed
    # because MLForge.tracing.reset() only resets the state for the current mode,
    # but this fixture runs when env var is at default.
    otel_trace._TRACER_PROVIDER = None
    otel_trace._TRACER_PROVIDER_SET_ONCE._done = False
    # Also reset MLForge's internal once flags for both modes
    provider._global_provider_init_once._done = False
    provider._isolated_tracer_provider_once._done = False


@pytest.mark.skipif(is_windows(), reason="Skipping as this is flaky on Windows")
def test_MLForge_and_opentelemetry_unified_tracing_with_otel_root_span(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "false")

    # Use set_destination to trigger tracer provider initialization
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id
    MLForge.tracing.set_destination(MLForgeExperimentLocation(experiment_id))

    otel_tracer = otel_trace.get_tracer(__name__)
    with otel_tracer.start_as_current_span("parent_span") as root_span:
        root_span.set_attribute("key1", "value1")
        root_span.add_event("event1", attributes={"key2": "value2"})

        # Active span id should be set
        assert MLForge.get_current_active_span().span_id == encode_span_id(root_span.context.span_id)

        with MLForge.start_span("MLForge_span") as MLForge_span:
            MLForge_span.set_inputs({"text": "hello"})
            MLForge_span.set_attributes({"key3": "value3"})

            with otel_tracer.start_as_current_span("child_span") as child_span:
                child_span.set_attribute("key4", "value4")
                child_span.set_status(otel_trace.Status(otel_trace.StatusCode.OK))

            MLForge_span.set_outputs({"text": "world"})

    traces = get_traces()
    assert len(traces) == 1
    trace = traces[0]
    assert trace.info.trace_id.startswith("tr-")  # trace ID should be in MLForge format
    assert trace.info.trace_id == MLForge.get_last_active_trace_id()
    assert trace.info.experiment_id == experiment_id
    assert trace.info.status == TraceState.OK
    assert trace.info.request_time == root_span.start_time // 1_000_000
    assert (
        abs(
            trace.info.execution_duration - (root_span.end_time - root_span.start_time) // 1_000_000
        )
        <= 1
    )
    assert trace.info.request_preview is None
    assert trace.info.response_preview is None

    spans = trace.data.spans
    assert len(spans) == 3
    assert spans[0].name == "parent_span"
    assert spans[0].attributes["key1"] == "value1"
    assert len(spans[0].events) == 1
    assert spans[0].events[0].name == "event1"
    assert spans[0].events[0].attributes["key2"] == "value2"
    assert spans[0].parent_id is None
    assert spans[0].status.status_code == SpanStatusCode.UNSET
    assert spans[1].name == "MLForge_span"
    assert spans[1].attributes["key3"] == "value3"
    assert spans[1].events == []
    assert spans[1].parent_id == spans[0].span_id
    assert spans[1].status.status_code == SpanStatusCode.OK
    assert spans[2].name == "child_span"
    assert spans[2].attributes["key4"] == "value4"
    assert spans[2].events == []
    assert spans[2].parent_id == spans[1].span_id
    assert spans[2].status.status_code == SpanStatusCode.OK


@pytest.mark.skipif(is_windows(), reason="Skipping as this is flaky on Windows")
def test_MLForge_and_opentelemetry_unified_tracing_with_MLForge_root_span(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "false")

    experiment_id = MLForge.set_experiment("test_experiment").experiment_id

    otel_tracer = otel_trace.get_tracer(__name__)
    with MLForge.start_span("MLForge_span") as MLForge_span:
        MLForge_span.set_inputs({"text": "hello"})

        with otel_tracer.start_as_current_span("otel_span") as otel_span:
            otel_span.set_attributes({"key3": "value3"})
            otel_span.set_status(otel_trace.Status(otel_trace.StatusCode.OK))

            with MLForge.start_span("child_span") as child_span:
                child_span.set_attribute("key4", "value4")

        MLForge_span.set_outputs({"text": "world"})

    traces = get_traces()
    assert len(traces) == 1
    trace = traces[0]
    assert trace.info.trace_id.startswith("tr-")  # trace ID should be in MLForge format
    assert trace.info.trace_id == MLForge.get_last_active_trace_id()
    assert trace.info.experiment_id == experiment_id
    assert trace.info.status == TraceState.OK
    assert trace.info.request_time == MLForge_span.start_time_ns // 1_000_000
    assert (
        abs(
            trace.info.execution_duration
            - (MLForge_span.end_time_ns - MLForge_span.start_time_ns) // 1_000_000
        )
        <= 1
    )
    assert trace.info.request_preview == '{"text": "hello"}'
    assert trace.info.response_preview == '{"text": "world"}'

    spans = trace.data.spans
    assert len(spans) == 3
    assert spans[0].name == "MLForge_span"
    assert spans[0].inputs == {"text": "hello"}
    assert spans[0].outputs == {"text": "world"}
    assert spans[0].status.status_code == SpanStatusCode.OK
    assert spans[1].name == "otel_span"
    assert spans[1].attributes["key3"] == "value3"
    assert spans[1].events == []
    assert spans[1].parent_id == spans[0].span_id
    assert spans[1].status.status_code == SpanStatusCode.OK
    assert spans[2].name == "child_span"
    assert spans[2].attributes["key4"] == "value4"
    assert spans[2].events == []
    assert spans[2].parent_id == spans[1].span_id
    assert spans[2].status.status_code == SpanStatusCode.OK


def test_MLForge_and_opentelemetry_isolated_tracing(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")

    experiment_id = MLForge.set_experiment("test_experiment").experiment_id

    # Set up otel tracer
    tracer_provider = TracerProvider(resource=None)
    exporter = InMemorySpanExporter()
    tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
    otel_trace.set_tracer_provider(tracer_provider)
    otel_tracer = otel_trace.get_tracer(__name__)

    with otel_tracer.start_as_current_span("otel_root") as root_span:
        root_span.set_attribute("key1", "value1")

        with MLForge.start_span("MLForge_root") as MLForge_span:
            MLForge_span.set_inputs({"text": "hello"})
            MLForge_span.set_outputs({"text": "world"})

            with otel_tracer.start_as_current_span("otel_child") as child_span:
                child_span.set_attribute("key2", "value2")

                with MLForge.start_span("MLForge_child") as MLForge_child_span:
                    MLForge_child_span.set_attribute("key3", "value3")

    traces = get_traces()
    assert len(traces) == 1
    trace = traces[0]
    assert trace is not None
    assert trace.info.experiment_id == experiment_id
    assert trace.info.trace_id.startswith("tr-")  # trace ID should be in MLForge format
    assert trace.info.status == TraceState.OK
    assert trace.info.request_time == MLForge_span.start_time_ns // 1_000_000
    assert (
        abs(
            trace.info.execution_duration
            - (MLForge_span.end_time_ns - MLForge_span.start_time_ns) // 1_000_000
        )
        <= 1
    )
    assert trace.info.request_preview == '{"text": "hello"}'
    assert trace.info.response_preview == '{"text": "world"}'

    spans = trace.data.spans
    assert len(spans) == 2
    assert spans[0].name == "MLForge_root"
    assert spans[0].inputs == {"text": "hello"}
    assert spans[0].outputs == {"text": "world"}
    assert spans[0].status.status_code == SpanStatusCode.OK
    assert spans[1].name == "MLForge_child"
    assert spans[1].attributes["key3"] == "value3"
    assert spans[1].status.status_code == SpanStatusCode.OK
    assert spans[1].parent_id == spans[0].span_id

    # Otel span should be exported independently of MLForge span
    otel_spans = exporter.get_finished_spans()
    assert len(otel_spans) == 2
    assert otel_spans[0].name == "otel_child"
    assert otel_spans[0].attributes["key2"] == "value2"
    assert otel_spans[0].parent.span_id == otel_spans[1].context.span_id
    assert otel_spans[1].name == "otel_root"
    assert otel_spans[1].attributes["key1"] == "value1"


def test_MLForge_adds_processors_to_existing_tracer_provider(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "false")
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id

    external_provider = TracerProvider()
    otel_trace.set_tracer_provider(external_provider)

    # Trigger MLForge initialization - this adds MLForge's processors to the external provider
    set_destination(MLForgeExperimentLocation(experiment_id))

    # Verify the external provider was NOT replaced
    assert otel_trace.get_tracer_provider() is external_provider

    # Verify MLForge's processors were added to the external provider
    processors = external_provider._active_span_processor._span_processors
    assert any(isinstance(p, MLForgeV3SpanProcessor) for p in processors)

    otel_tracer = otel_trace.get_tracer("external_lib")
    with otel_tracer.start_as_current_span("http_request_parent") as external_span:
        external_span.set_attribute("http.method", "GET")

        with MLForge.start_span("model_prediction") as MLForge_span:
            MLForge_span.set_inputs({"query": "test"})
            MLForge_span.set_outputs({"result": "success"})

    traces = get_traces()
    assert len(traces) == 1
    trace = traces[0]
    assert trace.info.trace_id.startswith("tr-")
    assert trace.info.status == TraceState.OK

    spans = trace.data.spans
    assert len(spans) == 2
    assert spans[0].name == "http_request_parent"
    assert spans[0].parent_id is None
    assert spans[1].name == "model_prediction"
    assert spans[1].parent_id == spans[0].span_id
    assert spans[1].inputs == {"query": "test"}
    assert spans[1].outputs == {"result": "success"}
    assert spans[1].status.status_code == SpanStatusCode.OK


def test_MLForge_does_not_add_duplicate_processors_global_mode(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "false")
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id

    external_provider = TracerProvider()
    otel_trace.set_tracer_provider(external_provider)

    # First call to initialize tracer provider - adds MLForge's processors
    set_destination(MLForgeExperimentLocation(experiment_id))

    processors = external_provider._active_span_processor._span_processors
    assert len(processors) == 1
    assert isinstance(processors[0], MLForgeV3SpanProcessor)

    # Second call to initialize tracer provider - should NOT add duplicate processors
    set_destination(MLForgeExperimentLocation(experiment_id))

    latest_processors = external_provider._active_span_processor._span_processors
    assert latest_processors == processors


def test_MLForge_does_not_add_duplicate_processors_isolated_mode(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id

    with MLForge.start_span("MLForge_span"):
        pass

    current_provider = provider.get()
    processors = current_provider._active_span_processor._span_processors
    assert len(processors) == 1
    assert isinstance(processors[0], MLForgeV3SpanProcessor)

    # Second call to initialize tracer provider - should NOT add duplicate processors
    set_destination(MLForgeExperimentLocation(experiment_id))

    latest_processors = current_provider._active_span_processor._span_processors
    assert latest_processors == processors


@pytest.mark.parametrize(
    "use_default_tracer_provider",
    [True, False],
)
def test_initialize_tracer_provider_without_otel_provider_set(
    monkeypatch, use_default_tracer_provider
):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, str(use_default_tracer_provider))
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id
    set_destination(MLForgeExperimentLocation(experiment_id))
    # no external provider set, we should always use MLForge own tracer provider
    processors = provider.get()._active_span_processor._span_processors
    assert len(processors) == 1
    assert isinstance(processors[0], MLForgeV3SpanProcessor)


def test_MLForge_span_does_not_leak_to_otel_context_by_default(monkeypatch):
    """Regression test for https://github.com/MLForge/MLForge/issues/24105

    In isolated tracer provider mode (the default), the MLForge span must NOT leak into the
    process-global OTel context. This preserves the isolation guarantee so unrelated OTel
    instrumentation (e.g. FastAPI, requests) does not accidentally nest under MLForge spans.
    """
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    monkeypatch.delenv(MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT.name, raising=False)
    MLForge.set_experiment("test_experiment")

    with MLForge.start_span(name="parent"):
        current = otel_trace.get_current_span()
        # Isolated mode keeps the MLForge span out of the global OTel context.
        assert not current.is_recording()
        assert isinstance(current, otel_trace.NonRecordingSpan)


def test_MLForge_trace_decorator_sets_otel_parent_context_when_opted_in(monkeypatch):
    """Regression test for https://github.com/MLForge/MLForge/issues/24105

    With MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT enabled, @MLForge.trace should propagate the
    span to the global OTel context so that pure-OTel libraries (e.g. strands-agents) can see
    it as a parent and create properly nested child spans.
    """
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    monkeypatch.setenv(MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT.name, "true")
    MLForge.set_experiment("test_experiment")

    captured = {}

    @MLForge.trace(name="parent")
    def my_function():
        current = otel_trace.get_current_span()
        captured["is_recording"] = current.is_recording()
        captured["is_non_recording"] = isinstance(current, otel_trace.NonRecordingSpan)
        return 42

    my_function()

    assert captured["is_recording"], "OTel current span should be recording inside @MLForge.trace"
    assert not captured["is_non_recording"]


def test_MLForge_start_span_sets_otel_parent_context_when_opted_in(monkeypatch):
    """Regression test for https://github.com/MLForge/MLForge/issues/24105

    With MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT enabled, MLForge.start_span() should propagate
    the span to the global OTel context so that pure-OTel libraries can nest under it.
    """
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    monkeypatch.setenv(MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT.name, "true")
    MLForge.set_experiment("test_experiment")

    with MLForge.start_span(name="parent"):
        current = otel_trace.get_current_span()
        is_recording = current.is_recording()
        is_non_recording = isinstance(current, otel_trace.NonRecordingSpan)

    assert is_recording, "OTel current span should be recording inside MLForge.start_span()"
    assert not is_non_recording


def test_MLForge_span_cleans_up_otel_context_after_exit(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    monkeypatch.setenv(MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT.name, "true")
    MLForge.set_experiment("test_experiment")

    with MLForge.start_span(name="parent"):
        inside = otel_trace.get_current_span()
        assert inside.is_recording()

    outside = otel_trace.get_current_span()
    assert not outside.is_recording(), (
        "OTel context should be cleaned up after the MLForge span exits"
    )


def test_nested_MLForge_spans_maintain_otel_context_when_opted_in(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    monkeypatch.setenv(MLForge_TRACE_PROPAGATE_TO_OTEL_CONTEXT.name, "true")
    MLForge.set_experiment("test_experiment")

    with MLForge.start_span(name="outer") as outer_span:
        outer_otel = otel_trace.get_current_span()
        assert outer_otel.is_recording()

        with MLForge.start_span(name="inner") as inner_span:
            inner_otel = otel_trace.get_current_span()
            assert inner_otel.is_recording()
            assert inner_span.parent_id == outer_span.span_id

        after_inner = otel_trace.get_current_span()
        assert after_inner.is_recording(), (
            "Outer span's OTel context should be restored after inner span exits"
        )


def test_get_bridged_tracer_provider_returns_MLForge_provider_isolated(monkeypatch):
    """get_bridged_tracer_provider should hand out MLForge's isolated provider by default.

    This lets OTel instrumentors that accept `tracer_provider=` route spans through MLForge's
    pipeline without depending on the process-global provider (issue #24105).
    """
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id
    set_destination(MLForgeExperimentLocation(experiment_id))

    bridged = get_bridged_tracer_provider()
    assert bridged is provider.get()
    processors = bridged._active_span_processor._span_processors
    assert any(isinstance(p, MLForgeV3SpanProcessor) for p in processors)


def test_get_bridged_tracer_provider_routes_spans_to_MLForge(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "true")
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id
    set_destination(MLForgeExperimentLocation(experiment_id))

    bridged = get_bridged_tracer_provider()
    otel_tracer = bridged.get_tracer("external_instrumentor")
    with otel_tracer.start_as_current_span("external_span") as span:
        span.set_attribute("key", "value")

    traces = get_traces()
    assert len(traces) == 1
    trace = traces[0]
    assert trace.info.trace_id.startswith("tr-")
    assert trace.info.experiment_id == experiment_id
    assert any(s.name == "external_span" for s in trace.data.spans)


def test_get_bridged_tracer_provider_returns_global_provider_unified(monkeypatch):
    monkeypatch.setenv(MLForge_USE_DEFAULT_TRACER_PROVIDER.name, "false")
    experiment_id = MLForge.set_experiment("test_experiment").experiment_id
    set_destination(MLForgeExperimentLocation(experiment_id))

    bridged = get_bridged_tracer_provider()
    assert bridged is otel_trace.get_tracer_provider()
