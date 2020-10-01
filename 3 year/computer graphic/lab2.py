from lab1 import np
from lab1 import get_file_data, get_points_and_edges
import matplotlib.pyplot as plt


def get_triangle_x_y(points, indexes):
    coords = []
    for i in range(1, 4):
        point = points[int(indexes[i]) - 1]
        coords.append(point)
    return coords


# def draw_triangles(points, edges, ax):
#     print(len(edges))
#     step = 0
#     for edge in edges[:1]:
#         x, y = get_triangle_x_y(points, edge)
#         ax.scatter(x, y, color='red', s=1)


def bresenham(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    condition = dy/dx
    if condition:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    delta = dy/dx
    #print(delta)
    error = 0.0
    ystep = 1 if y0 < y1 else -1
    y = y0
    points = []
    #print(x0_x1)
    print(x0)
    print(x1)
    for x in range(x0, x1):
        #print(f'x = {x}')
        points.append((y if condition else x, x if condition else y))
        #print(points)
        error += delta
        #print(error)
        if error >= 0.5:
            y += ystep
            error -= 1.0
    return np.array(points)


def draw_line(coords, ax, ind1, ind2):
    points = bresenham(coords[ind1][0], coords[ind1][1],
                       coords[ind2][0], coords[ind2][1]);
    #print(points)
    ax.scatter(points[:,0], points[:,1], s=1, c='r')


def draw_triangles(coords, ax):
    print(f'point1 = {coords[0]}')
    print(f'point2 = {coords[1]}')
    print(f'point3 = {coords[2]}')
    draw_line(coords, ax, 0, 1)
    draw_line(coords, ax, 1, 2)
    draw_line(coords, ax, 2, 0)
    # ax.scatter(coords[0][0], coords[0][1],c='b',s = 5)


def main():
    filename = 'teapot.obj'
    data = get_file_data(filename)
    points, edges = get_points_and_edges(data)
    print(points)
    # Take all x and y
    points = (points[:,1:-1].astype(float) * 100000).astype(int)
    print(points)
    fig, ax = plt.subplots()
    for edge in edges[:1]:
        coords = get_triangle_x_y(points, edge)
        draw_triangles(coords, ax)
    # draw_triangles(points, edges, ax)
    # ax.set_xbound(-4.0, 4.0)
    # ax.set_ybound(-4.0, 4.0)
    plt.show()


main()
