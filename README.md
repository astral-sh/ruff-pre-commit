# ruff-pre-commit

A [pre-commit](https://pre-commit.com/) hook for [Ruff](https://github.com/charliermarsh/ruff).

Distributed as a standalone repository to enable installing Ruff via prebuilt wheels from
[PyPI](https://pypi.org/project/ruff/).

### Using Ruff with pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/charliermarsh/ruff-pre-commit
  # Ruff version.
  rev: "v0.0.266"
  hooks:
    - id: ruff
```

Or, to enable autofix:

```yaml
- repo: https://github.com/charliermarsh/ruff-pre-commit
  # Ruff version.
  rev: "v0.0.266"
  hooks:
    - id: ruff
      args: [--fix, --exit-non-zero-on-fix]
```

Ruff's pre-commit hook should be placed after other formatting tools, such as Black and isort,
_unless_ you enable autofix, in which case, Ruff's pre-commit hook should run _before_ Black, isort,
and other formatting tools, as Ruff's autofix behavior can output code changes that require
reformatting.

## License

MIT
