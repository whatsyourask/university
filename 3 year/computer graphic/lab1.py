import numpy as np
from typing import Tuple, List


def get_file_data(filename) -> str:
    data = open(filename, 'r').read().split('\n')
    # Split data and cast it to list
    data = [elem.split(' ') for elem in data]
    # Remova emptry strings
    data.remove([''])
    data.remove([''])
    return np.array(data)


def get_max_min(points) -> Tuple:
    x = []
    y = []
    z = []
    for point in points:
        # Put all x in the list of x and so on with y and z
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


def find_start_f(data) -> int:
    # Count lines before first f
    line_number = 0
    for line in data:
        if 'f' in line:
            break
        else:
            line_number += 1
    return line_number


def get_points_and_edges(data):
    start_f = find_start_f(data)
    return data[:start_f], data[start_f:]


def surface_area(points) -> int:
    # Create matrices with ones
    matrix1 = np.ones((3, 3))
    matrix2 = np.ones((3, 3))
    matrix3 = np.ones((3, 3))
    # Cast list to np array and reshape it in matrix
    points = np.array(points).reshape(3, 3)
    # Copy by columns
    matrix1[:,1] = points[:,0]
    matrix1[:,2] = points[:,1]

    matrix2[:,1] = points[:,0]
    matrix2[:,2] = points[:,2]

    matrix3[:,1] = points[:,1]
    matrix3[:,2] = points[:,2]

    half = 0.5
    # Find determinants of matrices
    determ1 = np.linalg.det(matrix1)
    determ2 = np.linalg.det(matrix2)
    determ3 = np.linalg.det(matrix3)
    area = half * np.sqrt(determ1 ** 2 + determ2 ** 2 + determ3 ** 2)
    return area


def surface_area_all(points, edges) -> int:
    all = 0
    for edge in edges:
        ind1 = int(edge[1]) - 1
        ind2 = int(edge[2]) - 1
        ind3 = int(edge[3]) - 1
        all += surface_area([points[ind1][1:],
                             points[ind2][1:],
                             points[ind3][1:]])
    return all


def main():
    filename = 'teapot.obj'
    data     = get_file_data(filename)
    # Separate data like points and edges
    points, edges = get_points_and_edges(data)
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
    area = surface_area_all(points, edges)
    print(f'teapot area = {area}')


if __name__=='__main__':
    main()
