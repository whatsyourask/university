from backend import Parser
from typing import List


def write_to(file, data: List) -> None:
    open(file, 'w').write('\n'.join(data))


def output_count(description, data: List) -> None:
    print(description + ': ' + str(len(data)))


def main():
    filename = 'access.log'
    data = open(filename).read().split('\n')
    parser = Parser(data)
    http_begin = "HTTP/*.*\" "
    _401 = http_begin + "401"
    _401_results = parser.findall(_401)
    write_to('401.txt', _401_results)
    output_count('401', _401_results)
    _403 = http_begin + "403"
    _403_results = parser.findall(_403)
    write_to('403.txt', _403_results)
    output_count('403', _403_results)
    sql_select = "select +.+ +from"
    sql_select_results = parser.findall(sql_select)
    write_to('selects.txt', sql_select_results)
    output_count('selects', sql_select_results)
    sql_drop = "drop +.+"
    sql_drop_results = parser.findall(sql_drop)
    write_to('drop.txt', sql_drop_results)
    output_count('drop', sql_drop_results)
    sql_insert = "insert +into +.+ +values\(.+\)"
    sql_insert_results = parser.findall(sql_insert)
    write_to('inserts.txt', sql_insert_results)
    output_count('inserts', sql_insert_results)
    sql_exec = "exec +.+"
    sql_exec_results = parser.findall(sql_exec)
    write_to('execs.txt', sql_exec_results)
    output_count('execs', sql_exec_results)
    sql_delay = "(delay|sleep)\(.+\)"
    sql_delay_results = parser.findall(sql_delay)
    write_to('delays.txt', sql_delay_results)
    output_count('delays', sql_delay_results)
    url = " (/.*) HTTP/"
    times = "(:)(\d{1,2})" * 2 + " "
    dos_results = parser.find_by_time(url, times)
    write_to('dos.txt', dos_results)
    output_count('dos', dos_results)


if __name__=='__main__':
    main()
