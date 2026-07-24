from unittest import mock

import pytest

import MLForge.spark
from MLForge.exceptions import MLForgeException
from MLForge.spark.autologging import PythonSubscriber, _get_current_listener


@pytest.fixture
def mock_get_current_listener():
    with mock.patch(
        "MLForge.spark.autologging._get_current_listener", return_value=None
    ) as get_listener_patch:
        yield get_listener_patch


@pytest.mark.usefixtures("spark_session")
def test_autolog_call_idempotent():
    MLForge.spark.autolog()
    listener = _get_current_listener()
    MLForge.spark.autolog()
    assert _get_current_listener() == listener


def test_subscriber_methods():
    # Test that PythonSubscriber satisfies the contract expected by the underlying Scala trait
    # it implements (MLForgeAutologEventSubscriber)
    subscriber = PythonSubscriber()
    subscriber.ping()
    # Assert repl ID is stable & different between subscribers
    assert subscriber.replId() == subscriber.replId()
    assert PythonSubscriber().replId() != subscriber.replId()


def test_enabling_autologging_throws_for_wrong_spark_version(
    spark_session, mock_get_current_listener
):
    with mock.patch("MLForge.spark.autologging._get_spark_major_version", return_value=2):
        with pytest.raises(
            MLForgeException, match="Spark autologging unsupported for Spark versions < 3"
        ):
            MLForge.spark.autolog()


def test_spark_datasource_autologging_raise_on_databricks_serverless_shared_cluster(spark_session):
    for mock_fun in [
        "is_in_databricks_serverless_runtime",
        "is_in_databricks_shared_cluster_runtime",
    ]:
        with mock.patch(f"MLForge.utils.databricks_utils.{mock_fun}", return_value=True):
            MLForge.spark.autolog(disable=True)  # assert no error is raised.
            with pytest.raises(
                MLForgeException,
                match=(
                    "MLForge Spark dataset autologging is not supported on Databricks "
                    "shared clusters or Databricks serverless clusters."
                ),
            ):
                MLForge.spark.autolog()
