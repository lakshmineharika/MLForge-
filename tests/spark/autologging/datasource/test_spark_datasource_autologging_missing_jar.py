import pytest

import MLForge.spark
from MLForge.exceptions import MLForgeException

from tests.spark.autologging.utils import _get_or_create_spark_session


def test_enabling_autologging_throws_for_missing_jar():
    with _get_or_create_spark_session(jars=""):
        with pytest.raises(MLForgeException, match="ensure you have the MLForge-spark JAR attached"):
            MLForge.spark.autolog()
