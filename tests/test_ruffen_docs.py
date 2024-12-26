"""Test cases for ruffen_docs."""

# ruff: noqa: D103
from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from ruffen_docs import FormatterConfig, format_file_contents, main

if TYPE_CHECKING:
    from pathlib import Path

    from _pytest.capture import CaptureFixture

FORMATTER_MODE = FormatterConfig(
    target_version="py39",
    preview=False,
    configs=["line-length=88"],
)


def test_format_src_trivial() -> None:
    after, _ = format_file_contents("", FORMATTER_MODE)
    assert after == ""


def test_format_src_markdown_simple() -> None:
    before = dedent(
        """\
        ```python
        f(1,2,3)
        ```
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        ```python
        f(1, 2, 3)
        ```
        """,
    )


def test_format_src_markdown_leading_whitespace() -> None:
    before = dedent(
        """\
        ```   python
        f(1,2,3)
        ```
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        ```   python
        f(1, 2, 3)
        ```
        """,
    )


def test_format_src_markdown_python_after_newline() -> None:
    before = dedent(
        """\
        ```
        python --version
        echo "python"
        ```
        """,
    )
    after, errors = format_file_contents(before, FORMATTER_MODE)
    assert errors == []
    assert after == before


def test_format_src_markdown_short_name() -> None:
    before = dedent(
        """\
        ```   py
        f(1,2,3)
        ```
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        ```   py
        f(1, 2, 3)
        ```
        """,
    )


def test_format_src_markdown_options() -> None:
    before = dedent(
        """\
        ```python title='example.py'
        f(1,2,3)
        ```
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        ```python title='example.py'
        f(1, 2, 3)
        ```
        """,
    )


def test_format_src_markdown_trailing_whitespace() -> None:
    before = dedent(
        """\
        ```python
        f(1,2,3)
        ```    \n""",
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        ```python
        f(1, 2, 3)
        ```    \n""",
    )


def test_format_src_indented_markdown() -> None:
    before = dedent(
        """\
        - do this pls:
          ```python
          f(1,2,3)
          ```
        - also this
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        - do this pls:
          ```python
          f(1, 2, 3)
          ```
        - also this
        """,
    )


def test_format_src_markdown_pycon() -> None:
    before = dedent(
        """\
        hello

        ```pycon

            >>> f(1,2,3)
            output
        ```
        world
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        hello

        ```pycon

        >>> f(1, 2, 3)
        output
        ```
        world
        """,
    )


def test_format_src_markdown_pycon_after_newline() -> None:
    before = dedent(
        """\
        ```
        pycon is great
        >>> yes it is
        ```
        """,
    )
    after, errors = format_file_contents(before, FORMATTER_MODE)
    assert errors == []
    assert after == before


def test_format_src_markdown_pycon_options() -> None:
    before = dedent("""\
        hello

        ```pycon title='Session 1'

            >>> f(1,2,3)
            output
        ```
        world
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        hello

        ```pycon title='Session 1'

        >>> f(1, 2, 3)
        output
        ```
        world
        """)


def test_format_src_markdown_pycon_twice() -> None:
    before = dedent("""\
        ```pycon
        >>> f(1,2,3)
        output
        ```
        example 2
        ```pycon
        >>> f(1,2,3)
        output
        ```
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        ```pycon
        >>> f(1, 2, 3)
        output
        ```
        example 2
        ```pycon
        >>> f(1, 2, 3)
        output
        ```
        """)


def test_format_src_markdown_comments_disable() -> None:
    before = dedent("""\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_markdown_comments_disabled_enabled() -> None:
    before = dedent("""\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        ```python
        'double quotes rock'
        ```
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        ```python
        "double quotes rock"
        ```
        """)


def test_format_src_markdown_comments_before() -> None:
    before = dedent("""\
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        ```python
        'double quotes rock'
        ```
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        ```python
        "double quotes rock"
        ```
        """)


def test_format_src_markdown_comments_after() -> None:
    before = dedent("""\
        ```python
        'double quotes rock'
        ```
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        ```python
        "double quotes rock"
        ```
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        """)


def test_format_src_markdown_comments_only_on() -> None:
    # fmt: off
    before = dedent("""\
        <!-- blacken-docs:on -->
        ```python
        'double quotes rock'
        ```
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        <!-- blacken-docs:on -->
        ```python
        "double quotes rock"
        ```
        """,
    )
    # fmt: on


def test_format_src_markdown_comments_only_off() -> None:
    # fmt: off
    before = dedent("""\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        """,
    )
    # fmt: on
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_markdown_comments_multiple() -> None:
    before = dedent(
        """\
        "<!-- blacken-docs:on -->
        "  # ignored
        "<!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        <!-- blacken-docs:on -->
        "  # ignored
        "<!-- blacken-docs:off -->
        <!-- blacken-docs:off -->
        "  # ignored
        "```python
        'single quotes rock'
        ```
        """,  # no on comment, off until the end
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_on_off_comments_in_code_blocks() -> None:
    before = dedent("""\
        ````md
        <!-- blacken-docs:off -->
        ```python
        f(1,2,3)
        ```
        <!-- blacken-docs:on -->
        ````
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_markdown_comments_disable_pycon() -> None:
    before = dedent("""\
        <!-- blacken-docs:off -->
        ```pycon
        >>> 'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_latex_minted() -> None:
    before = dedent("""\
        hello
        \\begin{minted}{python}
        f(1,2,3)
        \\end{minted}
        world!""")
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        hello
        \\begin{minted}{python}
        f(1, 2, 3)
        \\end{minted}
        world!""")


def test_format_src_latex_minted_opt() -> None:
    before = dedent("""\
        maths!
        \\begin{minted}[mathescape]{python}
        # Returns $\\sum_{i=1}^{n}i$
        def sum_from_one_to(n):
          r = range(1, n+1)
          return sum(r)
        \\end{minted}
        done""")
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        maths!
        \\begin{minted}[mathescape]{python}
        # Returns $\\sum_{i=1}^{n}i$
        def sum_from_one_to(n):
            r = range(1, n + 1)
            return sum(r)
        \\end{minted}
        done""")


def test_format_src_latex_minted_indented() -> None:
    # Personally I would have minted python code all flush left,
    # with only the Python code's own four space indentation:
    before = dedent(
        """\
        hello
          \\begin{minted}{python}
            if True:
              f(1,2,3)
          \\end{minted}
        world!
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        hello
          \\begin{minted}{python}
          if True:
              f(1, 2, 3)
          \\end{minted}
        world!
        """,
    )


def test_format_src_latex_minted_pycon() -> None:
    before = dedent("""\
        Preceding text
        \\begin{minted}[gobble=2,showspaces]{pycon}
        >>> print( 'Hello World' )
        Hello World
        \\end{minted}
        Following text.""")
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        Preceding text
        \\begin{minted}[gobble=2,showspaces]{pycon}
        >>> print("Hello World")
        Hello World
        \\end{minted}
        Following text.""")


def test_format_src_latex_minted_pycon_indented() -> None:
    # Nicer style to put the \begin and \end on new lines,
    # but not actually required for the begin line
    before = dedent("""\
        Preceding text
          \\begin{minted}{pycon}
            >>> print( 'Hello World' )
            Hello World
          \\end{minted}
        Following text.""")
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        Preceding text
          \\begin{minted}{pycon}
          >>> print("Hello World")
          Hello World
          \\end{minted}
        Following text.""")


def test_format_src_latex_minted_comments_off() -> None:
    before = dedent("""\
        % blacken-docs:off
        \\begin{minted}{python}
        'single quotes rock'
        \\end{minted}
        % blacken-docs:on
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_latex_minted_comments_off_pycon() -> None:
    before = dedent("""\
        % blacken-docs:off
        \\begin{minted}{pycon}
        >>> 'single quotes rock'
        \\end{minted}
        % blacken-docs:on
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_pythontex() -> None:
    # fmt: off
    before = dedent("""\
        hello
        \\begin{pyblock}
        f(1,2,3)
        \\end{pyblock}
        world!""",
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        hello
        \\begin{pyblock}
        f(1, 2, 3)
        \\end{pyblock}
        world!""",
    )
    # fmt: on


def test_format_src_pythontex_comments_off() -> None:
    before = dedent("""\
        % blacken-docs:off
        \\begin{pyblock}
        f(1,2,3)
        \\end{pyblock}
        % blacken-docs:on
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst() -> None:
    before = dedent("""\
        hello

        .. code-block:: python

            f(1,2,3)

        world
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        hello

        .. code-block:: python

            f(1, 2, 3)

        world
        """)


def test_format_src_rst_empty() -> None:
    before = dedent("""\
    some text

    .. code-block:: python


    some other text
    """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst_literal_blocks() -> None:
    before = dedent(
        """\
        hello::

            f(1,2,3)

        world
        """,
    )
    after, _ = format_file_contents(
        before,
        FORMATTER_MODE,
        rst_literal_blocks=True,
    )
    assert after == dedent(
        """\
        hello::

            f(1, 2, 3)

        world
        """,
    )


def test_format_src_rst_literal_block_empty() -> None:
    before = dedent(
        """\
        hello::
        world
        """,
    )
    after, _ = format_file_contents(
        before,
        FORMATTER_MODE,
        rst_literal_blocks=True,
    )
    assert after == before


def test_format_src_rst_literal_blocks_nested() -> None:
    before = dedent(
        """
        * hello

          .. warning::

            don't hello too much
        """,
    )
    after, errors = format_file_contents(
        before,
        FORMATTER_MODE,
        rst_literal_blocks=True,
    )
    assert after == before
    assert errors == []


def test_format_src_rst_literal_blocks_empty() -> None:
    before = dedent(
        """
        Example::

        .. warning::

            There was no example.
        """,
    )
    after, errors = format_file_contents(
        before,
        FORMATTER_MODE,
        rst_literal_blocks=True,
    )
    assert after == before
    assert errors == []


def test_format_src_rst_literal_blocks_comments() -> None:
    before = dedent("""\
        .. blacken-docs:off
        Example::

            'single quotes rock'

        .. blacken-docs:on
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE, rst_literal_blocks=True)
    assert after == before


def test_format_src_rst_sphinx_doctest() -> None:
    before = dedent("""\
        .. testsetup:: group1

           import parrot
           mock = SomeMock( )

        .. testcleanup:: group1

           mock.stop( )

        .. doctest:: group1

           >>> parrot.voom( 3000 )
           This parrot wouldn't voom if you put 3000 volts through it!

        .. testcode::

           parrot.voom( 3000 )

        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. testsetup:: group1

           import parrot

           mock = SomeMock()

        .. testcleanup:: group1

           mock.stop()

        .. doctest:: group1

           >>> parrot.voom(3000)
           This parrot wouldn't voom if you put 3000 volts through it!

        .. testcode::

           parrot.voom(3000)

        """)


def test_format_src_rst_indented() -> None:
    before = dedent(
        """\
        .. versionadded:: 3.1

            hello

            .. code-block:: python

                def hi() -> None:
                    f(1,2,3)

            world
        """,
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        .. versionadded:: 3.1

            hello

            .. code-block:: python

                def hi() -> None:
                    f(1, 2, 3)

            world
        """,
    )


def test_format_src_rst_code_block_indent() -> None:
    before = dedent("""\
        .. code-block:: python

           f(1,2,3)
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: python

           f(1, 2, 3)
        """)


def test_format_src_rst_with_highlight_directives() -> None:
    before = dedent("""\
        .. code-block:: python
            :lineno-start: 10
            :emphasize-lines: 11

            def foo():
                bar(1,2,3)
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: python
            :lineno-start: 10
            :emphasize-lines: 11

            def foo():
                bar(1, 2, 3)
        """)


def test_format_src_rst_python_inside_non_python_code_block() -> None:
    before = dedent("""\
        blacken-docs does changes like:

        .. code-block:: diff

             .. code-block:: python

            -    'Hello World'

            +    "Hello World"
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst_python_comments() -> None:
    before = dedent("""\
        .. blacken-docs:off
        .. code-block:: python

            'single quotes rock'

        .. blacken-docs:on
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_integration_ok(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent("""\
        ```python
        f(1, 2, 3)
        ```
        """),
    )

    result = main((str(f),))

    assert result == 0
    assert not capsys.readouterr()[1]
    assert f.read_text() == dedent("""\
        ```python
        f(1, 2, 3)
        ```
        """)


def test_integration_modifies(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent("""\
        ```python
        f(1,2,3)
        ```
        """),
    )

    result = main((str(f),))

    assert result == 1
    out, _ = capsys.readouterr()
    assert out == f"{f}: Rewriting...\n"
    assert f.read_text() == dedent("""\
    ```python
    f(1, 2, 3)
    ```
    """)


def test_integration_line_length(tmp_path: Path) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent("""\
        ```python
        foo(very_very_very_very_very_very_very, long_long_long_long_long)
        ```
        """),
    )

    result = main((str(f), "--config", "line-length=80"))
    assert result == 0

    result2 = main((str(f), "--config", "line-length=50"))
    assert result2 == 1
    assert f.read_text() == dedent("""\
        ```python
        foo(
            very_very_very_very_very_very_very,
            long_long_long_long_long,
        )
        ```
        """)


def test_integration_check(tmp_path: Path) -> None:
    f = tmp_path / "f.md"
    text = dedent(
        """\
        ```python
        x = 'a' 'b'
        ```
        """,
    )
    f.write_text(text)

    result = main((str(f), "--check"))

    assert result == 1
    assert f.read_text() == text


def test_integration_preview(tmp_path: Path) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent(
            """\
            ```python
            x = 'a' 'b'
            ```
            """,
        ),
    )

    result = main((str(f), "--preview"))

    assert result == 1
    assert f.read_text() == dedent(
        """\
        ```python
        x = "ab"
        ```
        """,
    )


def test_integration_pyi(tmp_path: Path) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent(
            """\
            ```pyi
            class Foo: ...


            class Bar: ...
            ```
            """,
        ),
    )

    result = main((str(f),))

    assert result == 1
    assert f.read_text() == dedent(
        """\
        ```pyi
        class Foo: ...
        class Bar: ...
        ```
        """,
    )


def test_integration_filename_last(tmp_path: Path) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent("""\
        ```python
        def very_very_long_function_name(
            very_very_very_very_very_very,
            another_very_very_very_very_very_very,
            *long_long_long_long_long_long
        ):
            pass
        ```
        """),
    )

    result2 = main(("--config", "line-length=88", str(f)))

    assert result2 == 1
    assert f.read_text() == dedent("""\
        ```python
        def very_very_long_function_name(
            very_very_very_very_very_very,
            another_very_very_very_very_very_very,
            *long_long_long_long_long_long,
        ):
            pass
        ```
        """)


def test_integration_syntax_error(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent("""\
        ```python
        f(
        ```
        """),
    )

    result = main((str(f),))

    assert result == 2
    out, _ = capsys.readouterr()
    assert out.startswith(f"{f}:1: code block parse error")
    assert f.read_text() == dedent("""\
        ```python
        f(
        ```
        """)


def test_integration_ignored_syntax_error(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    f = tmp_path / "f.md"
    f.write_text(
        dedent("""\
        ```python
        f( )
        ```

        ```python
        f(
        ```
        """),
    )

    result = main((str(f), "--skip-errors"))

    assert result == 1
    out, _ = capsys.readouterr()
    assert f.read_text() == dedent("""\
        ```python
        f()
        ```

        ```python
        f(
        ```
        """)


def test_format_src_rst_jupyter_sphinx() -> None:
    before = dedent("""\
        hello

        .. jupyter-execute::

            f(1,2,3)

        world
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        hello

        .. jupyter-execute::

            f(1, 2, 3)

        world
        """)


def test_format_src_rst_jupyter_sphinx_with_directive() -> None:
    before = dedent("""\
        hello

        .. jupyter-execute::
            :hide-code:

            f(1,2,3)

        world
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        hello

        .. jupyter-execute::
            :hide-code:

            f(1, 2, 3)

        world
        """)


def test_format_src_python_docstring_markdown() -> None:
    before = dedent(
        '''\
        def f() -> None:
            """
            hello world

            ```python
            f(1,2,3)
            ```
            """
            pass
        ''',
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        '''\
        def f() -> None:
            """
            hello world

            ```python
            f(1, 2, 3)
            ```
            """
            pass
        ''',
    )


def test_format_src_python_docstring_rst() -> None:
    before = dedent(
        '''\
        def f() -> None:
            """
            hello world

            .. code-block:: python

                f(1,2,3)
            """
            pass
        ''',
    )
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        '''\
        def f() -> None:
            """
            hello world

            .. code-block:: python

                f(1, 2, 3)
            """
            pass
        ''',
    )


def test_format_src_rst_pycon() -> None:
    before = dedent("""\
        hello

        .. code-block:: pycon

            >>> f(1,2,3)
            output

        world
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        hello

        .. code-block:: pycon

            >>> f(1, 2, 3)
            output

        world
        """)


def test_format_src_rst_pycon_with_continuation() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> d = {
            ...   "a": 1,
            ...   "b": 2,
            ...   "c": 3,}

        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            >>> d = {
            ...     "a": 1,
            ...     "b": 2,
            ...     "c": 3,
            ... }

        """)


def test_format_src_rst_pycon_adds_continuation() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> d = {"a": 1,"b": 2,"c": 3,}

        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> d = {
            ...     "a": 1,
            ...     "b": 2,
            ...     "c": 3,
            ... }

        """,
    )


def test_format_src_rst_pycon_preserves_trailing_whitespace() -> None:
    before = dedent("""\
        hello

        .. code-block:: pycon

            >>> d = {"a": 1, "b": 2, "c": 3}



        world
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst_pycon_indented() -> None:
    before = dedent("""\
        .. versionadded:: 3.1

            hello

            .. code-block:: pycon

                >>> def hi():
                ...     f(1,2,3)
                ...

            world
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. versionadded:: 3.1

            hello

            .. code-block:: pycon

                >>> def hi():
                ...     f(1, 2, 3)
                ...

            world
        """)


def test_format_src_rst_pycon_code_block_is_final_line1() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...   pass
            ...
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...     pass
            ...
        """)


def test_format_src_rst_pycon_code_block_is_final_line2() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...   pass
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...     pass
            ...
        """)


def test_format_src_rst_pycon_nested_def1() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...     def f(): pass
            ...
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...     def f():
            ...         pass
            ...
        """)


def test_format_src_rst_pycon_nested_def2() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...     def f(): pass
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            >>> if True:
            ...     def f():
            ...         pass
            ...
        """)


def test_format_src_rst_pycon_empty_line() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> l = [
            ...
            ...     1,
            ... ]
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            >>> l = [
            ...     1,
            ... ]
        """)


def test_format_src_rst_pycon_preserves_output_indentation() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> 1 / 0
            Traceback (most recent call last):

              File "<stdin>", line 1, in <module>

            ZeroDivisionError: division by zero
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst_pycon_elided_traceback() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> 1 / 0
            Traceback (most recent call last):
              ...
            ZeroDivisionError: division by zero
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst_pycon_no_prompt() -> None:
    before = dedent("""\
        .. code-block:: pycon

            pass
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst_pycon_no_trailing_newline() -> None:
    before = dedent("""\
        .. code-block:: pycon

            >>> pass""")
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            >>> pass
        """)


def test_format_src_rst_pycon_comment_before_promopt() -> None:
    before = dedent("""\
        .. code-block:: pycon

            # Comment about next line
            >>> pass
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == dedent("""\
        .. code-block:: pycon

            # Comment about next line
            >>> pass
        """)


def test_format_src_rst_pycon_comments() -> None:
    before = dedent("""\
        .. blacken-docs:off
        .. code-block:: pycon

            >>> 'single quotes rock'

        .. blacken-docs:on
        """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before


def test_format_src_rst_pycon_empty() -> None:
    before = dedent("""\
    some text

    .. code-block:: pycon


    some other text
    """)
    after, _ = format_file_contents(before, FORMATTER_MODE)
    assert after == before
