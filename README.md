# ruff-pre-commit

A [pre-commit](https://pre-commit.com/) hook for [Ruff](https://github.com/charliermarsh/ruff).

Distributed as a standalone repository to enable installing ruff via prebuilt wheels from
[PyPI](https://pypi.org/project/ruff/).

For pre-commit: see https://github.com/pre-commit/pre-commit

For ruff: see https://github.com/charliermarsh/ruff

### Using ruff with pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: ''  # Use the sha / tag you want to point at
    hooks:
      - id: ruff
```

## License

MIT
