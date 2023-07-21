# ruff-pre-commit

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![image](https://img.shields.io/pypi/v/ruff/0.0.279.svg)](https://pypi.python.org/pypi/ruff)
[![image](https://img.shields.io/pypi/l/ruff/0.0.279.svg)](https://pypi.python.org/pypi/ruff)
[![image](https://img.shields.io/pypi/pyversions/ruff/0.0.279.svg)](https://pypi.python.org/pypi/ruff)
[![Actions status](https://github.com/astral-sh/ruff-pre-commit/workflows/main/badge.svg)](https://github.com/astral-sh/ruff-pre-commit/actions)

A [pre-commit](https://pre-commit.com/) hook for [Ruff](https://github.com/astral-sh/ruff).

Distributed as a standalone repository to enable installing Ruff via prebuilt wheels from
[PyPI](https://pypi.org/project/ruff/).

### Using Ruff with pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.0.279
  hooks:
    - id: ruff
```

Or, to enable autofix:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.0.279
  hooks:
    - id: ruff
      args: [--fix, --exit-non-zero-on-fix]
```

To run the hook on Jupyter Notebooks too:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.0.279
  hooks:
    - id: ruff
      types_or: [python, pyi, jupyter]
```

Ruff's pre-commit hook should be placed after other formatting tools, such as Black and isort,
_unless_ you enable autofix, in which case, Ruff's pre-commit hook should run _before_ Black, isort,
and other formatting tools, as Ruff's autofix behavior can output code changes that require
reformatting.

## License

MIT

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img src="https://raw.githubusercontent.com/astral-sh/ruff/main/assets/svg/Astral.svg">
  </a>
</div>
