import MLForge
from MLForge.utils.class_utils import _get_class_from_string


def test_get_class_from_string():
    assert _get_class_from_string("MLForge.MLForgeClient") == MLForge.MLForgeClient
