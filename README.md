# ruff-pre-commit

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![image](https://img.shields.io/pypi/v/ruff/0.8.0.svg)](https://pypi.python.org/pypi/ruff)
[![image](https://img.shields.io/pypi/l/ruff/0.8.0.svg)](https://pypi.python.org/pypi/ruff)
[![image](https://img.shields.io/pypi/pyversions/ruff/0.8.0.svg)](https://pypi.python.org/pypi/ruff)
[![Actions status](https://github.com/astral-sh/ruff-pre-commit/workflows/main/badge.svg)](https://github.com/astral-sh/ruff-pre-commit/actions)

A [pre-commit](https://pre-commit.com/) hook for [Ruff](https://github.com/astral-sh/ruff).

Distributed as a standalone repository to enable installing Ruff via prebuilt wheels from
[PyPI](https://pypi.org/project/ruff/).

### Using Ruff with pre-commit

To run Ruff's [linter](https://docs.astral.sh/ruff/linter) and [formatter](https://docs.astral.sh/ruff/formatter)
(available as of Ruff v0.0.289) via pre-commit, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.8.0
  hooks:
    # Run the linter.
    - id: ruff
    # Run the formatter.
    - id: ruff-format
```

To enable lint fixes, add the `--fix` argument to the lint hook:

```yaml
repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.8.0
  hooks:
    # Run the linter.
    - id: ruff
      args: [ --fix ]
    # Run the formatter.
    - id: ruff-format
```

To avoid running on Jupyter Notebooks, remove `jupyter` from the list of allowed filetypes:

```yaml
repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.8.0
  hooks:
    # Run the linter.
    - id: ruff
      types_or: [ python, pyi ]
      args: [ --fix ]
    # Run the formatter.
    - id: ruff-format
      types_or: [ python, pyi ]
```

When running with `--fix`, Ruff's lint hook should be placed _before_ Ruff's formatter hook, and
_before_ Black, isort, and other formatting tools, as Ruff's fix behavior can output code changes
that require reformatting.

When running without `--fix`, Ruff's formatter hook can be placed before or after Ruff's lint hook.

(As long as your Ruff configuration avoids any [linter-formatter incompatibilities](https://docs.astral.sh/ruff/formatter/#conflicting-lint-rules),
`ruff format` should never introduce new lint errors, so it's safe to run Ruff's format hook _after_
`ruff check --fix`.)

## License

ruff-pre-commit is licensed under either of

- Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in ruff-pre-commit by you, as defined in the Apache-2.0 license, shall be
dually licensed as above, without any additional terms or conditions.

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img src="https://raw.githubusercontent.com/astral-sh/ruff/main/assets/svg/Astral.svg">
  </a>
</div>
