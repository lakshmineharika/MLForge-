import logging
import os
import subprocess
from functools import lru_cache

import docker
import pytest
import requests
from packaging.version import Version

import MLForge

TEST_IMAGE_NAME = "test_image"
MLForge_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RESOURCE_DIR = os.path.join(MLForge_ROOT, "tests", "resources", "dockerfile")

docker_client = docker.from_env()

_logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def clean_up_docker():
    yield

    # Get all containers using the test image
    containers = docker_client.containers.list(filters={"ancestor": TEST_IMAGE_NAME})
    for container in containers:
        container.remove(force=True)

    # Clean up the image
    try:
        docker_client.images.remove(TEST_IMAGE_NAME, force=True)
    except docker.errors.ImageNotFound:
        pass

    # Clean up the build cache and volumes
    try:
        subprocess.check_call(["docker", "builder", "prune", "-a", "-f"])
    except subprocess.CalledProcessError as e:
        _logger.warning("Failed to clean up docker system: %s", e)


@lru_cache(maxsize=1)
def get_released_MLForge_version():
    url = "https://pypi.org/pypi/MLForge/json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    versions = [
        v for v in map(Version, data["releases"]) if not (v.is_devrelease or v.is_prerelease)
    ]
    return str(max(versions))


def save_model_with_latest_MLForge_version(flavor, extra_pip_requirements=None, **kwargs):
    """
    Save a model with overriding MLForge version from dev version to the latest released version.
    By default a model is saved with the dev version of MLForge, which is not available on PyPI.
    Usually we can be workaround this by adding --serve-wheel flag that starts local PyPI server,
    however, this doesn't work when installing dependencies inside Docker container. Hence, this
    function uses `extra_pip_requirements` to save the model with the latest released MLForge.
    """
    latest_MLForge_version = get_released_MLForge_version()
    if flavor == "langchain":
        kwargs["pip_requirements"] = [
            f"MLForge[gateway]=={latest_MLForge_version}",
            "langchain<1.1.0",
        ]
    else:
        extra_pip_requirements = extra_pip_requirements or []
        extra_pip_requirements.append(f"MLForge=={latest_MLForge_version}")
        if flavor == "lightgbm":
            # Adding pyarrow < 18 to prevent pip installation resolution conflicts.
            extra_pip_requirements.append("pyarrow<18")
        kwargs["extra_pip_requirements"] = extra_pip_requirements
    flavor_module = getattr(MLForge, flavor)
    flavor_module.save_model(**kwargs)
