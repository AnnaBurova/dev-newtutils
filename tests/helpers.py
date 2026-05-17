"""
Updated on 2026-05
Created on 2026-02

@author: NewtCode Anna Burova

Functions:
    def print_my_func_name(
        ) -> None
    def print_my_captured(
        captured
        ) -> None
    def format_set_to_str(
        input_set: set
        ) -> str

Test example:
    def test_function_example(self, capsys):
        print_my_func_name()

        input_dict = {
        }
        print("input_dict:", input_dict)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "file.txt")

            dirname_exists = os.path.exists(os.path.dirname(file_path))
            assert dirname_exists is True
            print("dirname_exists:", dirname_exists)

        dirname_exists = os.path.exists(os.path.dirname(file_path))
        assert dirname_exists is False
        print("dirname_exists:", dirname_exists)

        with pytest.raises(SystemExit) as exc_info:
            Newt.function(input_dict)
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        obscure_list = [
            "C:\\Users\\",
            "\\AppData\\Local\\Temp\\",
            "/tmp/",
            ]
        if sys.platform == "win32" and os.name == "nt":
            # On Windows
            file_obscure_name = "C:\\Users\\*******\\AppData\\Local\\Temp\\***********"
        else:
            file_obscure_name = "/tmp/***********"

        captured = capsys.readouterr()
        print_my_captured(captured)

        assert "Function:" \
        "\n============================================" \
        "\n" == captured.out

        assert "" == captured.out
        assert "" == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
        # assert "This line will not be printed" not in captured.out
        # assert "This line will not be printed" not in captured.err
"""

import inspect


def print_my_func_name(
        ) -> None:
    """ Print name of the current function. """

    frame = inspect.currentframe()

    if frame and frame.f_back:
        print("Function:", frame.f_back.f_code.co_name)
    else:
        print("Function: <unknown>")

    print("============================================")


def print_my_captured(
        captured
        ) -> None:
    """ ## Pretty-print captured standard output and error streams from pytest.

    Args:
        captured (CaptureResult):
            A pytest `CaptureResult` object returned by `capsys.readouterr()`.
            Must provide `.out` and `.err` attributes representing captured
            standard output and standard error text.
    """

    print()
    print("START=======================================")

    print("=====captured.out=====")
    if captured.out:
        print(captured.out)
    else:
        print("(no stdout captured)")

    print("=====captured.err=====")
    if captured.err:
        print(captured.err)
    else:
        print("(no stderr captured)")

    print("END=========================================")

    # print(captured)  # TODO


def format_set_to_str(
        input_set: set
        ) -> str:
    """ ## Format a set into a sorted, human-readable string.

    Sorts elements by their string representation
    and wraps them in curly braces, similar to set literal syntax.

    Args:
        input_set (set):
            The set to format.<br>
            Elements can be of any type that supports str() conversion.

    Returns:
        out (str):
            A string of sorted elements wrapped in curly braces.<br>
            Example: `{1, 2, abc}` or `{}` for an empty set.
    """

    return "{" + ", ".join(str(x) for x in sorted(input_set, key=str)) + "}"
