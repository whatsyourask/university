from lab1 import np, List
from lab1 import get_file_data, get_points_and_edges
import matplotlib.pyplot as plt


def get_triangle_x_y(points, indexes) -> List:
    coords = []
    for i in range(0, 3):
        point = points[indexes[i] - 1]
        coords.append(point)
    return coords


def set_pixel(pixels, y, x, color):
    pixels[y, x, :] = color


def bresenham(x0, y0, x1, y1, pixels, x_map_shift, y_map_shift):
    # Projections
    dx = x1 - x0
    dy = y1 - y0
    # Choose direction to draw
    x_direction = 1 if dx > 0 else -1 if dx < 0 else 0
    y_direction = 1 if dy > 0 else -1 if dy < 0 else 0
    # Need to make the signs x and y equal
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    # Then we can compare them to define the incline of line
    if dx > dy:
        # The line is long
        # That means that we need to draw it along X
        x_shift, y_shift = x_direction, 0
        min_d, max_d     = dy, dx
    else:
        # The line is high
        x_shift, y_shift = 0, y_direction
        min_d, max_d     = dx, dy
    # Initial values of x and y
    x, y             = x0, y0
    error, iteration = max_d/2, 0
    # Set a first pixel with appropriate shift in map
    set_pixel(pixels, -y + y_map_shift, -x + x_map_shift, [0, 255, 0])
    # While we don't get a iteration equal to max of dx and dy
    while iteration < max_d:
        # Reduce the error on min delta of dx and dy
        error -= min_d
        if error < 0:
            # Shift both x and y
            # and increase error on max delta of dx and dy
            error += max_d
            x     += x_direction
            y     += y_direction
        else:
            # Shift either x or y
            x += x_shift
            y += y_shift
        iteration += 1
        # Set a pixel in map
        set_pixel(pixels, -y + y_map_shift, -x + x_map_shift, [0, 255, 0])


def draw_triangle(coords, ax, pixels, x_shift, y_shift):
    bresenham(coords[0][0], coords[0][1],
              coords[1][0], coords[1][1],
              pixels, x_shift, y_shift)
    bresenham(coords[1][0], coords[1][1],
              coords[2][0], coords[2][1],
              pixels, x_shift, y_shift)
    bresenham(coords[2][0], coords[2][1],
              coords[0][0], coords[0][1],
              pixels, x_shift, y_shift)


def draw_teapot(points, edges, ax, scale, dimension, x_shift, y_shift):
    # Take all x and y
    # And scale them
    points = (points[:,0:-1] * scale).astype(np.int64)
    # Create a pixels map
    pixels = np.zeros(dimension, dtype=np.uint8)
    for edge in edges:
        # For each edge in edges
        # Find corresponding coordinates and draw triangle
        coords = get_triangle_x_y(points, edge)
        draw_triangle(coords, ax, pixels, x_shift, y_shift)
    pixels = np.flip(pixels, axis=1)
    ax.imshow(pixels)
    plt.show()
    plt.imsave('teapot.png', pixels)


def main():
    filename      = 'teapot.obj'
    data          = get_file_data(filename)
    points, edges = get_points_and_edges(data)
    fig, ax       = plt.subplots()
    scale         = 300
    dimension     = (1950, 1950, 3)
    x_shift       = 1030
    y_shift       = 1030
    draw_teapot(points, edges, ax, scale, dimension, x_shift, y_shift)


if __name__=='__main__':
    main()
