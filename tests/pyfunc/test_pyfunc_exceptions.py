import pytest

import MLForge
from MLForge.exceptions import MLForgeException


class UnpicklableModel(MLForge.pyfunc.PythonModel):
    def __init__(self, path):
        with open(path, "w+") as f:
            pass

        self.not_a_file = f


def test_pyfunc_unpicklable_exception(tmp_path):
    model = UnpicklableModel(tmp_path / "model.pkl")

    with pytest.raises(
        MLForgeException,
        match="Please save the model into a python file and use code-based logging method instead",
    ):
        MLForge.pyfunc.save_model(python_model=model, path=tmp_path / "model")
