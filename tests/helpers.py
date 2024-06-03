"""
Created on 2024-06

@author: NewtCode Anna Burova

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
        newt_print_function_name()

        NewtCons.error_msg("Test error", stop=False)

        captured = capsys.readouterr()
        newt_print_captured(captured)

        assert (
            "Function: test_error_msg_without_stop\n"
            f"{'-' * 72}"
            "\n"
        ) == captured.out

        assert (
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


def newt_print_function_name(
        ) -> None:
    """ Print name of the current function. """

    frame = inspect.currentframe()

    if frame and frame.f_back:
        func_name = frame.f_back.f_code.co_name
    else:
        func_name = "<unknown>"

    print(f"Function: {func_name}")

    print("-"*72)


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
