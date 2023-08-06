import sys
sys.path.append('D:\YandexDisk\IKIT\OP\Semester_1_Python\lab 6\project')
from package.finish import final
import numpy as np


def selection_sort(lst):
    for i in range(len(lst)):
        low_value_index = i
        for j in range(i + 1, len(lst)):
            if lst[low_value_index] > lst[j]:
                low_value_index = j
        lst[i], lst[low_value_index] = lst[low_value_index], lst[i]
    return lst


def selection_sort_for_ex(lst):
    """
    >>> selection_sort_for_ex([0, -1, -100, 50, 3])
    [-100, -1, 0, 3, 50]

    >>> selection_sort_for_ex([0, 0, 3, 2])
    [0, 0, 2, 3]

    """
    for i in range(len(lst)):
        low_value_index = i
        for j in range(i + 1, len(lst)):
            if lst[low_value_index] > lst[j]:
                low_value_index = j
        lst[i], lst[low_value_index] = lst[low_value_index], lst[i]
    return lst


if __name__ == "__main__":
    import doctest
    doctest.testmod()
