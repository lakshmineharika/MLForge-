# flavors

CLI and shared helpers for cooking [`MLForge/ml-package-versions.yml`](../../MLForge/ml-package-versions.yml), the config that drives MLForge's cross-version test matrix.

## Commands

```bash
# Generate the cross-version test matrix (used by CI).
uv run flavors matrix --help

# Bump maximum versions in ml-package-versions.yml and regenerate
# MLForge/ml_package_versions.py.
uv run flavors update --help
```

## Python API

```python
from flavors import load, get_released_versions

config = load("MLForge/ml-package-versions.yml")
for name, flavor in config.items():
    print(name, flavor.package_info.pip_release)
```
