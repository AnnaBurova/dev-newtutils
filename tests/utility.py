"""
Created on 2025-10

@author: NewtCode Anna Burova
"""

import newtutils as Newt

numbers = Newt.sorting_ids([3, 1, 2, 3])
print(numbers)
# [1, 2, 3]
words = Newt.sorting_ids(['b', 'a', 'b'])
print(words)
# ['a', 'b']
mixed = Newt.sorting_ids(['f', 4, 'a', 2, 'b', 1, 'a'])
print(mixed)
# ['a', 'b', 'f', 1, 2, 4]

data_dict = [
    {"name": "Bob"},
    {"name": "Alice", "age": 30},
    {"name": "Charlie", "age": 25},
    {"name": "Aska", "age": 25},
    ]
dict_default = Newt.sorting_dict_by_keys(data_dict)
print(dict_default)
# {'name': 'Bob'}
# {'name': 'Alice', 'age': 30}
# {'name': 'Charlie', 'age': 25}
# {'name': 'Aska', 'age': 25}
dict_age = Newt.sorting_dict_by_keys(data_dict, "age")
print(dict_age)
# {'name': 'Charlie', 'age': 25}
# {'name': 'Aska', 'age': 25}
# {'name': 'Alice', 'age': 30}
# {'name': 'Bob'}
dict_name = Newt.sorting_dict_by_keys(data_dict, "name")
print(dict_name)
# {'name': 'Alice', 'age': 30}
# {'name': 'Aska', 'age': 25}
# {'name': 'Bob'}
# {'name': 'Charlie', 'age': 25}
dict_age_name = Newt.sorting_dict_by_keys(data_dict, "age", "name")
print(dict_age_name)
# {'name': 'Aska', 'age': 25}
# {'name': 'Charlie', 'age': 25}
# {'name': 'Alice', 'age': 30}
# {'name': 'Bob'}
dict_reverse = Newt.sorting_dict_by_keys(data_dict, "age", "name", reverse=True)
print(dict_reverse)
# {'name': 'Bob'}
# {'name': 'Alice', 'age': 30}
# {'name': 'Charlie', 'age': 25}
# {'name': 'Aska', 'age': 25}
