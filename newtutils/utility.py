"""
Created on 2025-10

@author: NewtCode Anna Burova
"""

from typing import List, Any

def sorting_ids(json_input: List[Any]) -> List[Any]:
    """
    Remove duplicates from a list and return the sorted result.

    This function accepts a list of values, removes any duplicate entries,
    and returns a new list sorted in ascending order.

    Parameters:
        json_input (List[Any]):
            A list of items which can be of any type that supports comparison.

    Returns:
        json_output (List[Any]):
            A new list containing unique items from `json_input`,
            sorted in ascending order.
    """

    json_unique = list(set(json_input))

    # json_output = sorted(json_unique)
    strs = sorted(x for x in json_unique if isinstance(x, str))
    ints = sorted(x for x in json_unique if isinstance(x, int))

    json_output = strs + ints

    return json_output
