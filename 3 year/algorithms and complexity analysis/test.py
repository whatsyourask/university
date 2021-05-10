from sorting import *
from generation import *
import sys
from time import time


class TestSort:
    sorts = [insertion_sort,
             bubble_sort,
             selection_sort,
             shell_sort,
             quick_sort,
             merge_sort,
             heap_sort,
             radix_sort]
    gen_func = {'num': generate_numbers,
                'int': generate_integers,
                'str': generate_strings,
                'date': generate_dates}
    def run(self, data_length: int, type: str) -> None:
        data = self.gen_func[type](data_length)
        for sort_func in self.sorts:
            self._test_one(sort_func, data.copy())

    def _test_one(self, sort_func: callable, data: list) -> None:
        start = time()
        if sort_func == quick_sort:
            sort_func(data, 0, len(data) - 1)
        else:
            sort_func(data)
        end = time()
        diff = (end - start) * 1000
        print(f'{sort_func.__name__}:\n\tsize: {len(data)}\n\ttype: {type(data[0])}\n\ttime: {diff}')


def main():
    sizes = [50, 500, 5000, 50000, 500000]
    types = ['str', 'date']
    ts = TestSort()
    for type in types:
        for size in sizes:
            ts.run(size, type)


if __name__=='__main__':
    main()
