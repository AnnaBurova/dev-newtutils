"""
Created on 2024-06

@author: NewtCode Anna Burova

Functions:
    def is_supported_set(
        value: object,
        ) -> TypeGuard[set[SupportedTypes] | frozenset[SupportedTypes]]
"""

from __future__ import annotations

from typing import TypeGuard

SupportedTypes = (
      None
    | bool
    | str
    | int
    | float
    | tuple[object, ...]
    | list[object]
    | dict[object, object]
    | set[object]
    | frozenset[object]
)


def is_supported_set(
        value: object,
        ) -> TypeGuard[set[SupportedTypes] | frozenset[SupportedTypes]]:
    """ ## Check if a value is a set or frozenset containing supported types.

    Type guard function that narrows the type of `value` from `object` to
    `set[SupportedTypes] | frozenset[SupportedTypes]` when the check passes.
    This enables type-safe operations on set contents in conditional blocks.

    Args:
        value (object):
            The value to check. Can be any object type.

    Returns:
        out (bool):
            True if `value` is a set or frozenset
            (type is narrowed via TypeGuard),<br>
            otherwise False.

    Raises:
        TypeError:
            If `value` cannot be checked with isinstance (rare edge cases).

    Examples:
        ```
        >>> INTERN.is_supported_set({1, 2, 3})
        True
        >>> INTERN.is_supported_set(frozenset(["a", "b"]))
        True
        >>> INTERN.is_supported_set([1, 2, 3])
        False
        >>> INTERN.is_supported_set("not a set")
        False
        ```
    """

    return isinstance(value, (set, frozenset))
