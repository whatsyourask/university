import re
from typing import List, Callable
import itertools

class Parser:
    def __init__(self, data: List) -> None:
        self.__data = data

    def findall(self, regex: str) -> List:
        matched = []
        for line in self.__data:
            result = re.findall(regex, line, flags=re.IGNORECASE)
            if result:
                matched.append(line)
        return matched

    def find_by_time(self, url_regex: str, time_regex: str) -> List:
        urls = self.searchall(url_regex)
        times = self.searchall(time_regex)
        print(urls)

    def searchall(self, regex: str) -> List:
        ## IDEA:
        # return list(itertools.filterfalse(lambda line: re.search(regex, line, flags=re.IGNORECASE) is None, self.__data))
        matched = []
        for line in self.__data:
            result = re.search(regex, line, flags=re.IGNORECASE)
            if result:
                print(result.group())
                matched.append(result.group())
        return matched
