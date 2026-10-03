"""Edge-case checks for the yanked-release filter in mirror.py.

Run with:

    uv run --no-project --with packaging --with urllib3 test_mirror.py

No test framework and no network access: these are plain asserts, so the file
runs under a bare Python interpreter the same way mirror.py itself is a plain
script.
"""

import importlib.util
import sys
from pathlib import Path


def _load_mirror():
    """Import the sibling mirror.py so the real code is under test."""
    path = Path(__file__).parent / "mirror.py"
    spec = importlib.util.spec_from_file_location("mirror", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["mirror"] = module
    spec.loader.exec_module(module)
    return module


mirror = _load_mirror()
is_yanked = mirror.is_yanked


def _fake_response(releases):
    """A stand-in for urllib3's response so get_all_versions() runs offline."""
    return type(
        "Response",
        (),
        {
            "status": 200,
            "json": lambda self: {"releases": releases},
        },
    )()


def _versions_from(releases):
    """Call the real get_all_versions() against a fixed release payload."""
    original = mirror.urllib3.request
    mirror.urllib3.request = lambda *a, **k: _fake_response(releases)
    try:
        return [str(v) for v in mirror.get_all_versions()]
    finally:
        mirror.urllib3.request = original


def test_fully_yanked_release_is_skipped():
    files = [
        {"filename": "ruff-0.12.6-py3-none-manylinux.whl", "yanked": True},
        {"filename": "ruff-0.12.6.tar.gz", "yanked": True},
    ]
    assert is_yanked(files) is True


def test_partially_yanked_release_is_kept():
    """A release where only some files were yanked stays installable, so it stays."""
    files = [
        {"filename": "ruff-0.1.0.tar.gz", "yanked": False},
        {"filename": "ruff-0.1.0-broken.whl", "yanked": True},
    ]
    assert is_yanked(files) is False


def test_single_file_release_is_kept():
    """0.12.6-style releases ship one file; one good file is enough to install."""
    files = [{"filename": "ruff-0.12.6-py3-none-manylinux.whl", "yanked": False}]
    assert is_yanked(files) is False


def test_missing_yanked_key_counts_as_not_yanked():
    files = [{"filename": "ruff-0.1.0.tar.gz"}]
    assert is_yanked(files) is False


def test_empty_file_list_does_not_crash_and_is_not_yanked():
    """all([]) is True, so the bool(files) guard is what stops an empty release
    from being treated as yanked."""
    assert is_yanked([]) is False
    assert is_yanked([]) is not all([])


def test_get_all_versions_drops_fully_yanked_release():
    """End-to-end: the filter has to be wired into get_all_versions()."""
    releases = {
        "0.12.5": [{"filename": "ruff-0.12.5.tar.gz", "yanked": False}],
        "0.12.6": [{"filename": "ruff-0.12.6.tar.gz", "yanked": True}],
        "0.12.7": [{"filename": "ruff-0.12.7.tar.gz", "yanked": False}],
    }
    assert _versions_from(releases) == ["0.12.5", "0.12.7"]


def test_get_all_versions_keeps_partially_yanked_release():
    releases = {
        "0.12.5": [{"filename": "ruff-0.12.5.tar.gz", "yanked": False}],
        "0.12.6": [
            {"filename": "ruff-0.12.6.tar.gz", "yanked": False},
            {"filename": "ruff-0.12.6-broken.whl", "yanked": True},
        ],
    }
    assert _versions_from(releases) == ["0.12.5", "0.12.6"]


def test_get_all_versions_tolerates_release_with_no_files():
    releases = {
        "0.12.5": [{"filename": "ruff-0.12.5.tar.gz", "yanked": False}],
        "0.12.6": [],
    }
    assert _versions_from(releases) == ["0.12.5", "0.12.6"]


def test_get_all_versions_still_sorts():
    releases = {
        v: [{"filename": "f", "yanked": False}] for v in ["0.2.0", "0.10.0", "0.1.0"]
    }
    assert _versions_from(releases) == ["0.1.0", "0.2.0", "0.10.0"]


if __name__ == "__main__":
    for name, case in sorted(globals().items()):
        if name.startswith("test_") and callable(case):
            case()
            print(f"ok  {name}")
    print("\nall tests passed")
