from backend import Parser


def main():
    filename = 'access.log'
    data = open(filename).read().split('\n')
    parser = Parser(data)
    http_begin = "HTTP/*.*\" "
    _401 = http_begin + "401"
    _401_results = parser.findall(_401)
    print(_401_results)
    _403 = http_begin + "403"
    _403_results = parser.findall(_403)
    print(_403_results)
    sql_select = "select +.+ +from"
    sql_select_results = parser.findall(sql_select)
    print(sql_select_results)
    sql_drop = "drop +.+"
    sql_drop_results = parser.findall(sql_drop)
    print(sql_drop_results)
    sql_insert = "insert +into +.+ +values\(.+\)"
    sql_insert_results = parser.findall(sql_insert)
    print(sql_insert_results)
    sql_exec = "exec +.+"
    sql_exec_results = parser.findall(sql_exec)
    print(sql_exec_results)
    sql_delay = "(delay|sleep)\(.+\)"
    url = " (/.+)+ HTTP/"
    times = ":\d{2}:\d{2}:\d{2}"
    dos_results = parser.find_by_time(url, times)


if __name__=='__main__':
    main()
