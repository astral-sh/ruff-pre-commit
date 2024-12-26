# ruff-pre-commit

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![image](https://img.shields.io/pypi/v/ruff/0.8.4.svg)](https://pypi.python.org/pypi/ruff)
[![image](https://img.shields.io/pypi/l/ruff/0.8.4.svg)](https://pypi.python.org/pypi/ruff)
[![image](https://img.shields.io/pypi/pyversions/ruff/0.8.4.svg)](https://pypi.python.org/pypi/ruff)
[![Actions status](https://github.com/astral-sh/ruff-pre-commit/workflows/main/badge.svg)](https://github.com/astral-sh/ruff-pre-commit/actions)

A [pre-commit](https://pre-commit.com/) hook for [Ruff](https://github.com/astral-sh/ruff).

Distributed as a standalone repository to enable installing Ruff via prebuilt wheels from
[PyPI](https://pypi.org/project/ruff/).

## Using Ruff with pre-commit

To run Ruff's [linter](https://docs.astral.sh/ruff/linter) and [formatter](https://docs.astral.sh/ruff/formatter)
(available as of Ruff v0.0.289) via pre-commit, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.8.4
  hooks:
    # Run the linter.
    - id: ruff
    # Run the formatter.
    - id: ruff-format
    # Run the formatter on documentation files.
    - id: ruff-format-docs
```

To enable lint fixes, add the `--fix` argument to the lint hook:

```yaml
repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.8.4
  hooks:
    # Run the linter.
    - id: ruff
      args: [ --fix ]
    # Run the formatter.
    - id: ruff-format
    # Run the formatter on documentation files.
    - id: ruff-format-docs
```

To avoid running on Jupyter Notebooks, remove `jupyter` from the list of allowed filetypes:

```yaml
repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.8.4
  hooks:
    # Run the linter.
    - id: ruff
      types_or: [ python, pyi ]
      args: [ --fix ]
    # Run the formatter.
    - id: ruff-format
      types_or: [ python, pyi ]
    # Run the formatter on documentation files.
    - id: ruff-format-docs # ruff-format-docs does not support Jupyter Notebooks.
```

When running with `--fix`, Ruff's lint hook should be placed _before_ Ruff's formatter hook, and
_before_ Black, isort, and other formatting tools, as Ruff's fix behavior can output code changes
that require reformatting.

When running without `--fix`, Ruff's formatter hook can be placed before or after Ruff's lint hook.

(As long as your Ruff configuration avoids any [linter-formatter incompatibilities](https://docs.astral.sh/ruff/formatter/#conflicting-lint-rules),
`ruff format` should never introduce new lint errors, so it's safe to run Ruff's format hook _after_
`ruff check --fix`.)

## Docs Formatter

The ruff docs formatter is a command line tool that rewrites documentation files in place. It is based on Blacken-docs however it uses Ruff's formatter instead of Black to format code blocks. It supports Markdown, reStructuredText, and LaTex files. Additionally, you can run it on Python files to reformat Markdown and reStructuredText within docstrings.

When installed, run `ruff-format-docs` with the filenames to rewrite:

```sh
ruff-format-docs README.md
```

If any file is modified, `ruff-format-docs` exits nonzero.

`ruff-format-docs` does not have any ability to recurse through directories.
Use the pre-commit integration, globbing, or another technique for
applying to many files. For example, with `git ls-files | xargs`\_:

```sh
git ls-files -z -- '*.md' | xargs -0 ruff-format-docs
```

The ruff docs formatter currently passes the following options through to ruff:

- `--target-version` - The minimum Python version that should be supported.
- `--preview` - Enable preview mode; enables unstable formatting. Use `--no-preview` to disable.
- `--config`- Either a path to a TOML configuration file (`pyproject.toml` or `ruff.toml`), or a TOML `<KEY> = <VALUE>` pair (such as you might find in a `ruff.toml` configuration file) overriding a specific configuration option. Overrides of individual settings using this option always take precedence over all configuration files, including configuration files that were also specified using `--config`. Note, more than one `--config` option can be used at once.

It also has the below extra options:

- `--check` - Avoid writing any formatted code blocks back; instead, exit with a non-zero status code if any code blocks would have been modified, and zero otherwise.
- `--skip-errors` - Don't exit non-zero for errors from Ruff (normally syntax errors).
- `--rst-literal-blocks` - Also format literal blocks in reStructuredText files (more below).

### Supported code block formats

Ruff docs formatter formats code blocks matching the following patterns.

#### Markdown

In "python" blocks:

````markdown
```python
def hello():
    print("hello world")
```
````

"pycon" blocks:

````markdown
```pycon

>>> def hello():
...     print("hello world")
...

```
````

And pyi blocks:

````markdown
```pyi
def hello() -> None: ...
```
````

Prevent formatting within a block using `ruff-format-docs:off` and
`ruff-format-docs:on` comments:

````markdown
<!-- ruff-format-docs:off -->

```python
# whatever you want
```

<!-- ruff-format-docs:on -->
````

Within Python files, docstrings that contain Markdown code blocks may be
reformatted:

````python
def f():
    """docstring here

    ```python
    print("hello world")
    ```
    """
````

#### reStructuredText

In "python" blocks:

```rst
.. code-block:: python

    def hello():
        print("hello world")
```

In "pycon" blocks:

```rst
.. code-block:: pycon

    >>> def hello():
    ...     print("hello world")
    ...
```

Prevent formatting within a block using `ruff-format-docs:off` and
`ruff-format-docs:on` comments:

```rst
.. ruff-format-docs:off

.. code-block:: python

    # whatever you want

.. ruff-format-docs:on
```

Use `--rst-literal-blocks` to also format [literal
blocks](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#literal-blocks):

```rst
An example::

    def hello():
        print("hello world")
```

Literal blocks are marked with `::` and can be any monospaced text by
default. However Sphinx interprets them as Python code [by
default](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#rst-literal-blocks).
If your project uses Sphinx and such a configuration, add
`--rst-literal-blocks` to also format such blocks.

Within Python files, docstrings that contain reStructuredText code
blocks may be reformatted:

```python
def f():
    """docstring here

    .. code-block:: python

        print("hello world")
    """
```

#### LaTeX

In minted "python" blocks:

```latex
\begin{minted}{python}
def hello():
    print("hello world")
\end{minted}
```

In minted "pycon" blocks:

```latex
\begin{minted}{pycon}
>>> def hello():
...     print("hello world")
...
\end{minted}
```

In PythonTeX blocks:

```latex
\begin{pycode}
def hello():
    print("hello world")
\end{pycode}
```

Prevent formatting within a block using `ruff-format-docs:off` and
`ruff-format-docs:on` comments:

```latex
% ruff-format-docs:off
\begin{minted}{python}
# whatever you want
\end{minted}
% ruff-format-docs:on
```

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
    <img src="https://raw.githubusercontent.com/astral-sh/ruff/main/assets/svg/Astral.svg" alt="Made by Astral">
  </a>
</div>
