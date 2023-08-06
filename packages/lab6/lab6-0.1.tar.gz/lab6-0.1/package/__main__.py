import sys
sys.path.append(r'D:\YandexDisk\IKIT\OP\Semester_1_Python\lab 6\project')
import doctest
from package.selection_sort import selection_sort
from package.selection_sort import selection_sort_for_ex
from package.end import ending
from example import info
import numpy as np



def start():
    main_flag = None
    while main_flag != 'y':
        main_list = []
        len_list = input('Введите длинну списка: ')

        if not len_list.isdigit():
            print(f'Введите натуральное число. Введено {len_list}.')
            continue

        len_list = int(len_list)
        i = 0

        while i != len_list:
            list_item = input("Введите элемент списка: ")

            if not list_item.replace('-', '', 1).isdigit():
                print(f'Введите целое число. Введено {list_item}.')
                continue

            list_item = int(list_item)
            main_list.append(list_item)
            i += 1

        print(f'Исходный список длинной {len_list}: {main_list}.')
        main_list = selection_sort(main_list)

        stop_main = input(
            'Для продолжения нажмите любую клавишу. Для завершения введите y: \n')

        if stop_main.lower() == 'y':
            print('Программа завершена. Спасибо за сеанс!')


if __name__ == '__main__':
    start()
