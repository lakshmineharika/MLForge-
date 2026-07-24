# MLForge Skinny

`MLForge-skinny` a lightweight version of MLForge that is designed to be used in environments where you want to minimize the size of the package.

## Core Files

| File               | Description                                                                     |
| ------------------ | ------------------------------------------------------------------------------- |
| `MLForge`           | A symlink that points to the `MLForge` directory in the root of the repository.  |
| `pyproject.toml`   | The package metadata. Autogenerate by [`dev/pyproject.py`](../dev/pyproject.py) |
| `README_SKINNY.md` | The package description. Autogenerate by [`dev/skinny.py`](../dev/pyproject.py) |

## Installation

```sh
# If you have a local clone of the repository
pip install ./libs/skinny

# If you want to install the latest version from GitHub
pip install git+https://github.com/MLForge/MLForge.git#subdirectory=libs/skinny
```
