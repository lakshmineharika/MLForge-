import pytest

import MLForge


@pytest.mark.parametrize("version", ["2.7.1", "2.8.1"])
def test_backward_compatibility(version):
    model = MLForge.pyfunc.load_model(f"tests/resources/pyfunc_models/{version}")
    assert model.predict("MLForge is great!") == "MLForge is great!"
