from unittest import mock

import pytest

import MLForge
from MLForge.utils.rest_utils import MLForgeHostCreds

_DATABRICKS_UC_REGISTRY_URI = "databricks-uc"
_DATABRICKS_TRACKING_URI = "databricks"
_DATABRICKS_UC_OSS_REGISTRY_URI = "uc"
_REGISTRY_HOST_CREDS = MLForgeHostCreds("https://hello-registry")
_TRACKING_HOST_CREDS = MLForgeHostCreds("https://hello-tracking")


def mock_host_creds(uri):
    if uri == _DATABRICKS_TRACKING_URI:
        return _TRACKING_HOST_CREDS
    elif uri in (_DATABRICKS_UC_REGISTRY_URI, _DATABRICKS_UC_OSS_REGISTRY_URI):
        return _REGISTRY_HOST_CREDS
    raise Exception(f"Got unexpected store URI {uri}")


@pytest.fixture
def mock_databricks_uc_host_creds():
    with mock.patch(
        "MLForge.store._unity_catalog.registry.rest_store.get_databricks_host_creds",
        side_effect=mock_host_creds,
    ):
        yield


@pytest.fixture
def mock_databricks_uc_oss_host_creds():
    with mock.patch(
        "MLForge.store._unity_catalog.registry.uc_oss_rest_store.get_oss_host_creds",
        side_effect=mock_host_creds,
    ):
        yield


@pytest.fixture
def configure_client_for_uc(mock_databricks_uc_host_creds):
    """
    Configure MLForge client to register models to UC
    """
    with mock.patch("MLForge.utils.databricks_utils.get_databricks_host_creds"):
        orig_registry_uri = MLForge.get_registry_uri()
        MLForge.set_registry_uri("databricks-uc")
        yield
        MLForge.set_registry_uri(orig_registry_uri)
