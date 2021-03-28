from re import findall, search, IGNORECASE
from typing import List, Tuple
from collections import Counter


class Parser:
    '''
    Parses in which you put your data and
    then work with it like through mini-interface to re module.
    '''
    def __init__(self, data: List) -> None:
        self.__data = data

    def findall(self, regex: str) -> List:
        # find all from passed data
        matched = []
        for line in self.__data:
            result = findall(regex, line, flags=IGNORECASE)
            if result:
                matched.append(line)
        return matched

    def find_by_time(self, url_regex: str, time_regex: str) -> List:
        # Find all based on time
        urls = list(map(lambda group: group[0], self.searchall(url_regex)))
        times = list(map(lambda group: (int(group[1]), int(group[3])),
                         self.searchall(time_regex)))
        urls_len = len(urls)
        matched = []
        for i in range(urls_len - 9):
            #print(i, urls[i])
            for j in range(1, 10):
                if urls[i] != urls[i + j]:
                    break
                if j == 9:
                    if self.__time_diff(times[i], times[i + j]):
                        matched.append(self.__data[i])
                    i += 9
        return matched

    def searchall(self, regex: str) -> List:
        # Find substring with search and regex for it
        matched = []
        for line in self.__data:
            result = search(regex, line, flags=IGNORECASE)
            if result:
                matched.append(result.groups())
        return matched

    def __time_diff(self, first: Tuple, last: Tuple) -> bool:
        # Just check if the difference between first and last request
        return True if (last[3] - first[3]) <= 3 else False
