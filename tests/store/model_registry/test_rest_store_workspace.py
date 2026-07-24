from unittest import mock

import pytest

from MLForge.exceptions import MLForgeException
from MLForge.store.model_registry.rest_store import RestStore
from MLForge.utils.rest_utils import MLForgeHostCreds

ACTIVE_WORKSPACE = "team-a"


def test_model_registry_rest_store_workspace_guard():
    creds = MLForgeHostCreds("https://hello")
    store = RestStore(lambda: creds)
    store._workspace_support = False

    with mock.patch(
        "MLForge.store.workspace_rest_store_mixin.get_request_workspace",
        return_value=ACTIVE_WORKSPACE,
    ):
        with pytest.raises(
            MLForgeException,
            match="Active workspace 'team-a' cannot be used because the remote server does not",
        ):
            store.search_registered_models()
