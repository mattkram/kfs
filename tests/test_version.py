from pathlib import Path

import pytest
import toml

import kfs


@pytest.fixture()
def version_from_pyproject_toml(project_root_dir: Path) -> str:
    with (project_root_dir / "pyproject.toml").open("r") as fp:
        data = toml.load(fp)
    return data["tool"]["poetry"]["version"]


def test_version(version_from_pyproject_toml: str) -> None:
    """Check that the version of the installed package matches pyproject.toml."""
    assert kfs.__version__ == version_from_pyproject_toml
