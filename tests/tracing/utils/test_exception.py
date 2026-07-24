import pytest

from MLForge.exceptions import MLForgeTracingException
from MLForge.tracing.utils.exception import raise_as_trace_exception


def test_raise_as_trace_exception():
    @raise_as_trace_exception
    def test_fn():
        raise ValueError("error")

    with pytest.raises(MLForgeTracingException, match="error"):
        test_fn()

    @raise_as_trace_exception
    def test_fn_no_raise():
        return 0

    assert test_fn_no_raise() == 0
