# Regression test for https://github.com/MLForge/MLForge/issues/21779:
# MLForge-skinny users couldn't use MLForge.anthropic.autolog() because importing
# MLForge.types.chat transitively pulled in numpy via
# MLForge.types.__init__ -> MLForge.types.llm -> MLForge.types.schema.

import importlib.util
import os

import pytest


@pytest.fixture(autouse=True)
def is_skinny():
    if "MLForge_SKINNY" not in os.environ:
        pytest.skip("This test is only valid for the skinny client")


def test_MLForge_types_chat_importable_without_numpy():
    # Verify numpy is genuinely not installed (not just not yet imported)
    assert importlib.util.find_spec("numpy") is None

    # This import chain was failing before the fix:
    # MLForge.types.chat -> MLForge.types.__init__ -> MLForge.types.llm -> MLForge.types.schema -> numpy
    from MLForge.types.chat import ChatMessage  # noqa: F401
