"""
Created on 2025-10

@author: NewtCode Anna Burova
"""

from typing import List, Dict, Any


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


def sorting_dict_by_keys(
    data: List[Dict[str, Any]],
    *keys: str,
    reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Sort a list of dictionaries by one or more keys.
    Dictionaries missing a key are placed at the end.

    Parameters:
        data (List[Dict[str, Any]]):
            The list of dictionaries to sort.
        *keys (str):
            Keys to sort by, in priority order.
        reverse (bool): by default False
            If True, sort in descending order.

    Returns:
        List[Dict[str, Any]]
            A new list sorted by the given keys. Dictionaries missing a key
            are placed at the end.
    """

    def sort_key(d: Dict[str, Any]):
        result = []

        for key in keys:
            value = d.get(key, None)
            # None goes to the end
            result.append((value is None, value))

        return tuple(result)

    return sorted(data, key=sort_key, reverse=reverse)
