# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "packaging==23.1",
#   "urllib3==2.0.5",
# ]
# ///
"""Update ruff-pre-commit to the latest version of ruff."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any

import tomllib
import urllib3
from packaging.requirements import Requirement
from packaging.version import Version

if TYPE_CHECKING:
    from collections.abc import Sequence

ROOT_DIR = Path(__file__).parent


def main() -> None:
    """Update ruff-pre-commit to the latest version of ruff."""
    with (ROOT_DIR / "pyproject.toml").open("rb") as f:
        pyproject = tomllib.load(f)

    all_versions = get_all_versions()
    current_version = get_current_version(pyproject=pyproject)
    target_versions = [v for v in all_versions if v > current_version]

    for version in target_versions:
        paths = process_version(version)
        if subprocess.check_output(["git", "status", "-s"]).strip():
            subprocess.run(["git", "add", *paths], check=True)
            subprocess.run(["git", "commit", "-m", f"Mirror: {version}"], check=True)
            subprocess.run(["git", "tag", f"v{version}"], check=True)
        else:
            print(f"No change v{version}")


def get_all_versions() -> list[Version]:
    """Fetch all versions of ruff from pypi."""
    response = urllib3.request("GET", "https://pypi.org/pypi/ruff/json")
    if response.status != 200:
        raise RuntimeError("Failed to fetch versions from pypi")

    versions = [Version(release) for release in response.json()["releases"]]
    return sorted(versions)


def get_current_version(pyproject: dict[str, Any]) -> Version:
    """Get the current version of ruff from pyproject.toml."""
    requirements = [Requirement(d) for d in pyproject["project"]["dependencies"]]
    requirement = next((r for r in requirements if r.name == "ruff"), None)
    assert requirement is not None, "pyproject.toml does not have ruff requirement"

    specifiers = list(requirement.specifier)
    assert (
        len(specifiers) == 1 and specifiers[0].operator == "=="
    ), f"ruff's specifier should be exact matching, but `{requirement}`"

    return Version(specifiers[0].version)


def process_version(version: Version) -> Sequence[str]:
    """Update the version of ruff in pyproject.toml and README.md."""

    def replace_pyproject_toml(content: str) -> str:
        return re.sub(r'"ruff==.*"', f'"ruff=={version}"', content)

    def replace_readme_md(content: str) -> str:
        content = re.sub(r"rev: v\d+\.\d+\.\d+", f"rev: v{version}", content)
        return re.sub(r"/ruff/\d+\.\d+\.\d+\.svg", f"/ruff/{version}.svg", content)

    paths = {
        ROOT_DIR / "pyproject.toml": replace_pyproject_toml,
        ROOT_DIR / "README.md": replace_readme_md,
    }

    for path, replacer in paths.items():
        content = path.read_text()
        updated_content = replacer(content)
        path.write_text(updated_content)

    return tuple([str(path) for path in paths])


if __name__ == "__main__":
    main()
