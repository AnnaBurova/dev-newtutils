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
