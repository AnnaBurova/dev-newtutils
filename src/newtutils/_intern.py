"""
Created on 2024-06

@author: NewtCode Anna Burova

Functions:
    def is_supported_type(
        value: object,
        ) -> TypeGuard[
              tuple[SupportedTypes, ...]
            | list[SupportedTypes]
            | dict[str, SupportedTypes]
            | set[SupportedTypes]
            | frozenset[SupportedTypes]
        ]
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


def is_supported_type(
        value: object,
        ) -> TypeGuard[
              tuple[SupportedTypes, ...]
            | list[SupportedTypes]
            | dict[str, SupportedTypes]
            | set[SupportedTypes]
            | frozenset[SupportedTypes]
        ]:
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
    """

    is_type = isinstance(value, (
        tuple,
        list,
        dict,
        set,
        frozenset,
    ))

    return is_type
