# ruff-pre-commit

A [pre-commit](https://pre-commit.com/) hook for [Ruff](https://github.com/charliermarsh/ruff).

Distributed as a standalone repository to enable installing Ruff via prebuilt wheels from
[PyPI](https://pypi.org/project/ruff/).

For pre-commit: see https://github.com/pre-commit/pre-commit

For Ruff: see https://github.com/charliermarsh/ruff

### Using Ruff with pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/charliermarsh/ruff-pre-commit
  # Ruff version.
  rev: 'v0.0.257'
  hooks:
    - id: ruff
```

Or, to enable autofix:

```yaml
- repo: https://github.com/charliermarsh/ruff-pre-commit
  # Ruff version.
  rev: 'v0.0.257'
  hooks:
    - id: ruff
      args: [--fix, --exit-non-zero-on-fix]
```

Note that Ruff's pre-commit hook should run before Black, isort, and other
formatting tools.

## License

MIT
