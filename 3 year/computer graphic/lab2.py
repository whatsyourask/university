from lab1 import np
from lab1 import get_file_data, get_points_and_edges
import matplotlib.pyplot as plt


def get_triangle_x_y(points, indexes):
    x, y = [], []
    for i in range(1, 4):
        point = points[int(indexes[i]) - 1]
        x.append(point[0])
        y.append(point[1])
    return x, y


def draw_triangles(points, edges, ax):
    print(len(edges))
    for edge in edges[:100]:
        x, y = get_triangle_x_y(points, edge)
        ax.scatter(x, y, color='red', s=1)
    exit(0)

def main():
    filename = 'teapot.obj'
    data = get_file_data(filename)
    points, edges = get_points_and_edges(data)
    print(points)
    # Take all x and y
    points = points[:,1:-1]
    print(points)
    fig, ax = plt.subplots()
    draw_triangles(points, edges, ax)
    ax.set_xbound(0.0, 4.0)
    ax.set_ybound(0.0, 4.0)
    plt.show()


main()
