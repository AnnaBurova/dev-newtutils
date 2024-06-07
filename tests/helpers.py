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

        assert newt_calc_str_len_with_path_type(0, captured.out)
        assert newt_calc_str_len_with_path_type(0, captured.err)
        assert len(captured.out) == 0
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


def newt_calc_str_len_with_path_type(
        expected_len: int,
        captured_out: str
        ) -> bool:
    """ Calculate output length after normalizing Path type representation lengths. """

    path_type_text = str(type(Path(".")))
    path_type_length = len(path_type_text)
    path_type_count = captured_out.count(path_type_text)

    REFERENCE_PATH_TYPE_LENGTH = 29

    normalized_output_length = (
        len(captured_out)
        - path_type_count * path_type_length
        + path_type_count * REFERENCE_PATH_TYPE_LENGTH
    )

    return normalized_output_length == expected_len
