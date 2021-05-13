from typing import List


def insertion_sort(array: List) -> List:
    length = len(array)
    for i in range(1, length):
        current = array[i]
        prev_ind = i - 1
        while prev_ind >= 0 and current < array[prev_ind]:
            array[prev_ind + 1] = array[prev_ind]
            prev_ind -= 1
        array[prev_ind + 1] = current
    return array


def bubble_sort(array: List) -> List:
    length = len(array)
    for i in range(length):
        for j in range(0, length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def selection_sort(array: List) -> List:
    length = len(array)
    for i in range(length):
        min_ind = i
        for j in range(i + 1, length):
            if array[min_ind] > array[j]:
                min_ind = j
        array[i], array[min_ind] = array[min_ind], array[i]
    return array


def shell_sort(array: List) -> List:
    length = len(array)
    gap = length // 2
    while gap > 0:
        for i in range(gap, length):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
        gap //= 2
    return array


def quick_sort(array: List, start: int, end: int) -> List:
    def partition(array: List, start: int, end: int) -> int:
        i = start - 1
        x = array[end]
        for j in range(start, end):
            if array[j] <= x:
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[end] = array[end], array[i + 1]
        return i + 1
    length = end - start + 1
    stack = [0] * length
    top = -1
    top += 1
    stack[top] = start
    top += 1
    stack[top] = end
    while top >= 0:
        end = stack[top]
        top -= 1
        start = stack[top]
        top -= 1
        p = partition(array, start, end)
        if p - 1 > start:
            top += 1
            stack[top] = start
            top += 1
            stack[top] = p - 1
        if p + 1 < end:
            top += 1
            stack[top] = p + 1
            top += 1
            stack[top] = end
    return array


def merge_sort(array: List) -> List:
    length = len(array)
    if length > 1:
        middle = length // 2
        left = array[:middle]
        right = array[middle:]
        merge_sort(left)
        merge_sort(right)
        i = 0
        j = 0
        k = 0
        left_length = len(left)
        right_length = len(right)
        while i < left_length and j < right_length:
            if left[i] < right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1
        while i < left_length:
            array[k] = left[i]
            i += 1
            k += 1
        while j < right_length:
            array[k] = right[j]
            j += 1
            k += 1
    return array


def heap_sort(array: List) -> List:
    def find_root(array: List, length: int, ind: int):
        root = ind
        left = 2 * ind + 1
        right = 2 * ind + 2
        if left < length and array[root] < array[left]:
            root = left
        if right < length and array[root] < array[right]:
            root = right
        if root != ind:
            array[ind], array[root] = array[root], array[ind]
            find_root(array, length, root)
    length = len(array)
    for i in range(length // 2 - 1, -1, -1):
        find_root(array, length, i)
    for i in range(length - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        find_root(array, i, 0)
    return array


def count_sort_letters(array, size, col, base):
    output   = [0] * size
    count    = [0] * base
    min_base = 0
    for item in array:
        correct_index = min(len(item) - 1, col)
        letter = ord(item[-(correct_index + 1)]) - min_base
        count[letter] += 1
    for i in range(base - 1):
        count[i + 1] += count[i]
    for i in range(size - 1, -1, -1):
        item = array[i]
        correct_index = min(len(item) - 1, col)
        letter = ord(item[-(correct_index + 1)]) - min_base
        output[count[letter] - 1] = item
        count[letter] -= 1
    return output


def radix_sort_letters(array):
    size = len(array)
    max_col = len(max(array, key = len))
    for col in range(max_col):
        array = count_sort_letters(array, size, col, 8034)
    return array


def radix_sort(array: List) -> List:
    def counting_sort(array: List[int], place: int, d: int=None):
        length = len(array)
        radix = 10
        result = [0] * length
        count = [0] * radix
        for i in range(length):
            count[(array[i] // place) % radix] += 1
        for i in range(1, radix):
            count[i] += count[i - 1]
        for i in range(length - 1, -1, -1):
            ind = array[i] // place
            result[count[ind % radix] - 1] = array[i]
            count[ind % 10] -= 1
        for i in range(length):
            array[i] = result[i]
    if type(array[0]) == int or type(array[0]) == float:
        largest = max(array)
        place = 1
        while largest // place > 0:
            counting_sort(array, place)
            place *= 10
        return array
    if type(array[0]) == str:
        return radix_sort_letters(array)


def ljust_desc(description: str) -> str:
    return description.ljust(30, ' ')


def main():
    array = [5, 7, -3, 10, 1, -5, 125, -52, 25, 10000, 0, 333, -123456]
    print(ljust_desc('initial array:'), array.copy(), '\n')
    print(ljust_desc('Insertion sort:'), insertion_sort(array.copy()))
    print(ljust_desc('Bubble sort:'), bubble_sort(array.copy()))
    print(ljust_desc('Selection sort:'), selection_sort(array.copy()))
    print(ljust_desc('Shell sort:'), shell_sort(array.copy()))
    print(ljust_desc('Quick sort:'), quick_sort(array.copy(), 0, len(array) - 1))
    print(ljust_desc('Merge sort:'), merge_sort(array.copy()))
    print(ljust_desc('Heap sort:'), heap_sort(array.copy()))
    print(ljust_desc('Radix sort:'), radix_sort(array.copy()))
    str_array = ['bbbbb', 'cccc', 'aaaaaaa', 'zzzzzz', 'eeeee', 'dddd']
    print(ljust_desc('Radix sort with strings:'), radix_sort(str_array.copy()))
    str_array = ['Hello', 'world', 'And', 'all', 'Of', 'you', 'friends']
    print(ljust_desc('Radix sort with strings:'), radix_sort(str_array.copy()))
    str_array.sort()
    print(ljust_desc('Python str array sort:'), str_array)


if __name__=='__main__':
    main()
