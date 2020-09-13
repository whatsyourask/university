import numpy as np


def get_file_data(filename):
    f    = open(filename, 'r')
    data = f.read()
    return data


def get_max_min(points):
    x = []
    y = []
    z = []
    for point in points:
        x.append(point[1])
        y.append(point[2])
        z.append(point[3])
    max_x = max(x)
    min_x = min(x)
    max_y = max(y)
    min_y = min(y)
    max_z = max(z)
    min_z = min(z)
    return max_x, min_x, max_y, min_y, max_z, min_z


def find_start_f(data):
    line_number = 0
    for line in data:
        if 'f' in line:
            break
        else:
            line_number += 1
    return line_number


def surface_area(point1, point2, point3):
    pass


def surface_area_all(points, edges):
    all = 0
    for edge in edges:
        ind1 = int(edge[1]) - 1
        ind2 = int(edge[2]) - 1
        ind3 = int(edge[3]) - 1
        all += surface_area(points[ind1], points[ind2], points[ind3])
    return all


def main():
    filename = 'teapot.obj'
    data     = get_file_data(filename).split('\n')
    data     = [elem.split(' ') for elem in data]
    data.remove([''])
    data.remove([''])
    data    = np.array(data)
    start_f = find_start_f(data)
    points  = data[:start_f]
    edges   = data[start_f:]
    points_count, edges_count = len(points), len(edges)
    print(f'points count: {points_count}')
    print(f'edges count: {edges_count}')
    max_min = get_max_min(points)
    print(f'max x = {max_min[0]}')
    print(f'min x = {max_min[1]}')
    print(f'max y = {max_min[2]}')
    print(f'min y = {max_min[3]}')
    print(f'max z = {max_min[4]}')
    print(f'min z = {max_min[5]}')
    surface_area_all(points, edges)


if __name__=='__main__':
  main()
