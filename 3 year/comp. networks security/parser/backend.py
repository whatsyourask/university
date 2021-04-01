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

        requests_counts = [1 for i in range(urls_len)]
        for i in range(urls_len):
            for j in range(i + 1, urls_len):
                if self.__time_diff(times[i], times[j]):
                    if urls[i] == urls[j]:
                        requests_counts[i] += 1
                else:
                    break
        matched = []
        for i in range(urls_len):
            if requests_counts[i] > 10:
                matched.append(self.__data[i])
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
        secs_diff = last[0] - first[0] == 0 and last[1] - first[1] <= 3
        one_min_diff = last[0] - first[0] == 1 and last[1] + 60 - first[1] <= 3
        return True if (secs_diff or one_min_diff) else False
