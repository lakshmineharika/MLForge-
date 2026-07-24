import os

import pytest


@pytest.mark.skipif(
    "MLForge_SKINNY" not in os.environ, reason="This test is only valid for the skinny client"
)
def test_autolog_without_scipy():
    import MLForge

    with pytest.raises(ImportError, match="scipy"):
        import scipy  # noqa: F401

    assert not MLForge.models.utils.HAS_SCIPY

    MLForge.autolog()
    MLForge.models.utils._Example({})
