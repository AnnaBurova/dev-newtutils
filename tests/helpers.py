"""
Created on 2024-06

@author: NewtCode Anna Burova

Constants:
    EXAMPLE_LIST (list)

Functions:
    def newt_print_function_name(
        ) -> None
    def newt_print_captured(
        captured: CaptureResult[str],
        print_full_captured: bool = True
        ) -> None

Test example:
    def test_function_example(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        func_name = newt_print_function_name()

        with pytest.raises(SystemExit) as exc_info:
            # TODO
            print("This line will not be printed")
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        # TODO

        captured = capsys.readouterr()
        newt_print_captured(captured)
        # newt_print_captured(captured, False)

        assert (
            f"Function: {func_name}\n"
            f"{'-' * 72}"
            "\n"
        ) == captured.out

        assert (
            "\x1b[1m\x1b[31m"
            "\nLocation: Unknown"
            "\n::: ERROR :::"
            "\nTest error"
            "\n\x1b[0m"
            "\n"
        ) == captured.err

        assert captured.err.count("\n::: ERROR :::\n") == 1

        # Expected absence of result
        assert "::: ERROR :::" not in captured.out
        assert "::: ERROR :::" not in captured.err
        assert "This line will not be printed" not in captured.out
        assert "This line will not be printed" not in captured.err
"""

import inspect
from _pytest.capture import CaptureResult

EXAMPLE_LIST: list[object] = [
    # None
    None,
    # bool
    False,
    # str
    "hello",
    # int
    42,
    # float
    3.14,
    # tuple[object, ...]
    ("hello", "hi", 42, ),
    # list[object]
    ["hello", "hi", 42],
    # dict[object, object]
    {"hello": 42, "hi": 3.14},
    # set[object]
    {3, 1, 2},
    # frozenset[object]
    frozenset({3, 1, 2}),
]


def newt_print_function_name(
        ) -> str:
    """ Print name of the current function. """

    frame = inspect.currentframe()

    if frame and frame.f_back:
        func_name = frame.f_back.f_code.co_name
    else:
        func_name = "<unknown>"

    print(f"Function: {func_name}")

    print("-"*72)

    return func_name


def newt_print_captured(
        captured: CaptureResult[str],
        print_full_captured: bool = True
        ) -> None:
    """ Pretty-print captured stdout and stderr. """

    print()
    print("="*72+" START")

    print("="*53+" captured.out "+"="*5)
    if captured.out:
        print(captured.out)
    else:
        print("(no stdout captured)")

    print("="*53+" captured.err "+"="*5)
    if captured.err:
        print(captured.err)
    else:
        print("(no stderr captured)")

    print("="*72+" END")

    if print_full_captured:
        print(captured)
