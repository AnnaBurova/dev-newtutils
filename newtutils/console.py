"""
Created on 2025-10

@author: NewtCode Anna Burova
"""

from colorama import Fore, Style


def error_msg(*args: object, stop: bool = True) -> None:
    """
    Print error messages in red to the console and optionally stop the program.

    This function prints one or more messages in bright red color using colorama.
    It can be used for CLI tools, scripts, or any console-based feedback.

    Parameters:
        *args (object): One or more messages or objects to print.
        stop (bool): by default True.

    Returns:
        None

    Raises:
        SystemExit: If stop=True, terminates the program with exit code 1.
    """

    message = "\n".join(str(arg) for arg in args)

    print(Style.BRIGHT, Fore.RED)
    print("::: ERROR :::")
    print(message)
    print(Style.RESET_ALL)

    if stop:
        raise SystemExit(1)
