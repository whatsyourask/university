from lab1 import np, List
from lab1 import get_file_data, get_points_and_edges
import matplotlib.pyplot as plt


class Lab2:
    """Class to draw the teapot"""
    def __init__(self, points, edges) -> None:
        self.points      = points[:,:2]
        self.edges       = edges
        self._scale      = None
        self._size       = None
        self._bg_color   = None
        self._draw_color = None

    @property
    def scale(self) -> int:
        return self._scale

    @scale.setter
    def scale(self, scale: int) -> None:
        self._scale = scale

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int) -> None:
        self._size = size

    @property
    def bg_color(self) -> List:
        return self._bg_color

    @bg_color.setter
    def bg_color(self, bg_color: List) -> None:
        self._bg_color = bg_color

    @property
    def draw_color(self) -> List:
        return self._draw_color

    @draw_color.setter
    def draw_color(self, draw_color) -> None:
        self._draw_color = draw_color

    def draw_teapot(self) -> None:
        self.pixels = np.full((self.size, self.size, 3),
                              self.bg_color,
                              dtype=np.uint8)
        for edge in self.edges:
            # For each edge in edges
            # Find corresponding coordinates and draw triangle
            coords = self._get_triangle_x_y(edge)
            self._draw_triangle(coords)

    def get_scalable_points(self) -> None:
        # Get abs of minimum x
        x_min_abs = np.fabs(self.points[:, 0].min())
        self.points[:, 0] += x_min_abs
        self.points[:, 1] *= -1
        # Get abs of minimum y
        y_min_abs          = np.fabs(self.points[:, 1].min())
        self.points[:, 1] += y_min_abs
        # Scale the coordinates
        self.points        = (self.points * self.scale).astype(np.int32)
        # Calculate center from size of figure
        self.center        = self.size // 2
        # Calculate center of x and y on the picture
        x_center, y_center = np.mean(self.points, axis=0, dtype=np.int32)
        # Shifting them to corresponded center
        self.points[:, 0] += self.center - x_center
        self.points[:, 1] += self.center - y_center
        # Get the point of the center
        self.center        = np.array([self.center, self.center])

    def _get_triangle_x_y(self, indexes) -> List:
        coords = []
        for i in range(3):
            point = self.points[indexes[i] - 1]
            coords.append(point)
        return coords

    def _draw_triangle(self, coords: List) -> None:
        self._bresenham(coords[0][0], coords[0][1],
                  coords[1][0], coords[1][1])
        self._bresenham(coords[1][0], coords[1][1],
                  coords[2][0], coords[2][1],)
        self._bresenham(coords[2][0], coords[2][1],
                  coords[0][0], coords[0][1])

    def _bresenham(self, x0, y0, x1, y1):
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
        self.pixels[y, x, :] = self.draw_color
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
            self.pixels[y, x, :] = self.draw_color

    def display(self) -> None:
        fig, ax = plt.subplots()
        ax.imshow(self.pixels)
        plt.show()
        plt.imsave('teapot.png', self.pixels)


def main():
    filename           = 'teapot.obj'
    data               = get_file_data(filename)
    points, edges      = get_points_and_edges(data)
    lab2               = Lab2(points, edges)
    lab2.scale         = 300
    lab2.size          = 2500
    lab2.bg_color      = [255, 255, 255]
    lab2.draw_color    = [255, 0, 0]
    lab2.get_scalable_points()
    lab2.draw_teapot()
    lab2.display()


if __name__=='__main__':
    main()
