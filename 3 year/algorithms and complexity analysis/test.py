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
             radix_sort,
             sorted]
    gen_random_func = {'num': generate_numbers,
                       'int': generate_integers,
                       'str': generate_strings,
                       'date': generate_dates}
    gen_half_sorted_func = {'num': generate_half_sorted_numbers,
                            'int': generate_half_sorted_integers,
                            'str': generate_half_sorted_strings,
                            'date': generate_half_sorted_dates}
    gen_reversed_sorted_func = {'num': generate_reversed_sorted_numbers,
                                'int': generate_reversed_sorted_integers,
                                'str': generate_reversed_sorted_strings,
                                'date': generate_reversed_sorted_dates}
    sizes = [50, 500, 5000, 50000, 500000]
    types = ['num', 'int', 'str', 'date']
    filename = 'report.txt'
    def test(self):
        self.f = open(self.filename, 'w')
        try:
            self.gen_func = self.gen_random_func
            print('Test with fully random data:')
            self.f.write('Test with fully random data:\n')
            self._test_one_generation()
            self.gen_func = self.gen_half_sorted_func
            print('Test with half sorted half random data:')
            self.f.write('Test with half sorted half random data:\n')
            self._test_one_generation()
            self.gen_func = self.gen_reversed_sorted_func
            print('Test with reverse order sorted data:')
            self.f.write('Test with reverse order sorted data:\n')
            self._test_one_generation()
        except Exception as error:
            print(error)
            self.f.write(error + '\n')
        finally:
            self.f.close()

    def _test_one_generation(self):
        for type in self.types:
            for size in self.sizes:
                self._test_one_size(size, type)

    def _test_one_size(self, data_length: int, type: str) -> None:
        if self.gen_func[type] in self.gen_half_sorted_func.values():
            data = self.gen_func[type](data_length, 0.8)
        else:
            data = self.gen_func[type](data_length)
        for sort_func in self.sorts:
            if data_length >= 50000 and sort_func in (insertion_sort, bubble_sort, selection_sort):
                continue
            if data_length > 50000 and sort_func == quick_sort:
                continue
            self._test_one_sort(sort_func, data.copy())

    def _test_one_sort(self, sort_func: callable, data: list) -> None:
        start = time()
        if sort_func == quick_sort:
            sort_func(data, 0, len(data) - 1)
        else:
            sort_func(data)
        end = time()
        diff = (end - start) * 1000
        print(f'{sort_func.__name__}:\n\tsize: {len(data)}\n\ttype: {type(data[0])}\n\ttime: {diff}')
        self.f.write(f'{sort_func.__name__}:\n\tsize: {len(data)}\n\ttype: {type(data[0])}\n\ttime: {diff}\n')


def main():
    sizes = [50, 500, 5000, 50000, 500000]
    types = ['num', 'int', 'str', 'date']
    ts = TestSort()
    ts.test()


if __name__=='__main__':
    main()
