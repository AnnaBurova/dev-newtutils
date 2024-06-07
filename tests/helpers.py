"""
Created on 2024-06

@author: NewtCode Anna Burova

Constants:
    EXAMPLE_LIST (list)
    EMPTY_LIST (list)

Functions:
    def newt_print_function_name(
        ) -> str
    def newt_print_captured(
        captured: CaptureResult[str],
        print_full_captured: bool = True
        ) -> None

Test example:
    def test_function_example(
            self,
            capsys: pytest.CaptureFixture[str]
            ) -> None:
        # TODO
        func_name = newt_print_function_name()

        change_variable = False

        NewtCons.error_msg(
            "Test error",
            location=f"{__name__} > {func_name}",
            stop=False
        )

        exc_info = 0
        with pytest.raises(SystemExit) as exc_info:
            # TODO
            change_variable = True
        assert exc_info.value.code == 1
        print("exc_info:", exc_info.value.code)

        # TODO

        captured = capsys.readouterr()
        newt_print_captured(captured)  # TODO
        # newt_print_captured(captured, False)

        min_captured_out_len = len(
            f"Function: {func_name}\n"
            f"{'-' * 72}"
            "\n"
        )

        assert len(captured.out) == min_captured_out_len
        assert len(captured.err) == 0

        assert captured.err.count("::: ERROR :::") == len(variable)

        # Expected absence of result
        assert change_variable is False
        assert captured.out.count("::: ERROR :::") == 0
        assert captured.err.count("::: ERROR :::") == 0
"""

import inspect
from _pytest.capture import CaptureResult
from pathlib import Path

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
    # pathlib
    Path("/home") / "user" / "project",
]

EMPTY_LIST: list[object] = [
    # None
    None,
    # bool
    False,
    # str
    "",
    # int
    0,
    # float
    0.0,
    # tuple[object, ...]
    tuple(),
    # list[object]
    list(),
    # dict[object, object]
    dict(),
    # set[object]
    set(),
    # frozenset[object]
    frozenset(),
    # pathlib
    Path(""),
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
        print()
        print(captured)
        print()
        print("len(captured):     ", len(captured) == 2)
        print("len(captured.out): ", len(captured.out))
        print("len(captured.err): ", len(captured.err))
        print()
