def insertion_sort(array: list) -> list:
    """
    1. Iterate from 1 to n
    2. Compare current with previous element
    3. If the current element is smaller, compare element before previous element
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
    2. Consider the last element as element in the right place and go through elements from 0 to the last element
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
    1. Go throug each element
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


def ljust_desc(description: str) -> str:
    return description.ljust(20, ' ')


def main():
    array = [5, 7, 10, 1, -5, 125, -52, 25, 10000, 0, 333]
    print(ljust_desc('initial array:'), array, '\n')
    print(ljust_desc('Insertion sort:'), insertion_sort(array))
    print(ljust_desc('Bubble sort:'), bubble_sort(array))
    print(ljust_desc('Selection sort:'), selection_sort(array))
    print(ljust_desc('Shell sort:'), shell_sort(array))


if __name__=='__main__':
    main()
