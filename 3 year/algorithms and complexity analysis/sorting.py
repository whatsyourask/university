def insertion_sort(array: list) -> list:
    """
    1. Iterate from 1 to n
    2. Compare current with the previous element
    3. If the current element is smaller, compare the element before the previous element
    """
    length = len(array)
    for i in range(1, length):
        current = array[i]
        prev_ind = i - 1
        while prev_ind >= 0 and current < array[prev_ind]:
            array[prev_ind + 1] = array[prev_ind]
            prev_ind -= 1
        array[prev_ind + 1] = current
    return array


def bubble_sort(array: list) -> list:
    """
    1. Go through from 0 to n - 1
    2. Consider the last element as an element in the right place and go through elements from 0 to the last element
    3. Swap if the element found is greater than the next
    """
    length = len(array)
    for i in range(length):
        for j in range(0, length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def selection_sort(array: list) -> list:
    """
    1. Go through each element
    2. Find the minimum element in the remaining
    3. Swap the first element with the found minimum
    """
    length = len(array)
    for i in range(length):
        min_ind = i
        for j in range(i + 1, length):
            if array[min_ind] > array[j]:
                min_ind = j
        array[i], array[min_ind] = array[min_ind], array[i]
    return array


def shell_sort(array: list) -> list:
    """
    1. Start with a gap equals to n / 2
    2. Do a gap insertion for this gap size
    3. Add a[i] to the gap sorted elements
    4. Make a space at i position
    5. Shift earlier gap-sorted elements
    6. Put a[i] that was taken above and place it in the right place
    7. Keep adding elements until the entire array is gap sorted
    """
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


def quick_sort(array: list, start: int, end: int) -> list:
    """
    1. If start is less than end then start sorting
    2. Find the pivot element with partition() function
    3. Start sorting part before the pivot and after it
    """
    def partition(array: list, start: int, end: int) -> int:
        """
        1. Go from start to end
        2. Go through elements while each element is less than or equal to the pivot
        3. Go from the end and search for an element that will be less than the pivot
        4. If start < end then swap elements at this indices
        5. After main loop swap pivot with the element at end index
        """
        pivot_ind = start
        pivot = array[pivot_ind]
        length = len(array)
        while start < end:
            while start < length and array[start] <= pivot:
                start += 1
            while array[end] > pivot:
                end -= 1
            if start < end:
                array[start], array[end] = array[end], array[start]
        array[end], array[pivot_ind] = array[pivot_ind], array[end]
        return end
    if start < end:
        pivot = partition(array, start, end)
        quick_sort(array, start, pivot - 1)
        quick_sort(array, pivot + 1, end)
    return array


def merge_sort(array: list) -> list:
    """
    1. If length is greater than 1 then start sorting
    2. Find the middle of the array
    3. Divide the array into 2 parts and sort each of them
    4. Copy results properly in result array and return it
    """
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


def heap_sort(array: list) -> list:
    """
    1. Go from the middle in decrease order and call find_root for each index
    2. Extract elements with swap and call find_root
    """
    def find_root(array: list, length: int, ind: int):
        """
        1. Initialize the root
        2. left = 2 * i + 1
        3. right = 2 * i + 2
        4. Check if the childs exist and are greater than root
        5. Change root if needed with swap
        6. Call find_root again
        """
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


def radix_sort(array: list) -> list:
    length = len(str(max(array)))
    rang = 10
    for i in range(length):
        B = [[] for k in range(rang)] #список длины range, состоящий из пустых списков
        for x in array:
            figure = x // 10**i % 10
            B[figure].append(x)
        array = []
        for k in range(rang):
            array = array + B[k]
    return array


def ljust_desc(description: str) -> str:
    return description.ljust(20, ' ')


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


if __name__=='__main__':
    main()
