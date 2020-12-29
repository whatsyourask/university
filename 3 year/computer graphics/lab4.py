from lab3 import np, plt, Lab3
import json
from typing import List, Dict


class Lab4(Lab3):
    def __init__(self, digits: Dict, count: int, p_count) -> None:
        self._digits  = digits
        self._count   = count
        self._p_count = p_count

    def _get_centered_coords(self):
        self._get_all_coords_in_one_matrix()
        # Calculate the center of x and y
        x_center, y_center = np.mean(np.mean(self._points, axis=1), axis=0)
        # Then calculate the difference between
        # center on the frame and centers of coordinates
        self._center  = self._size // 2
        self._d_x = self._center - x_center
        self._d_y = self._center - y_center

    def _get_all_coords_in_one_matrix(self):
        self._points = []
        # Take the digit that will be as { 'digit_0' : { ... }}
        for digit in self._digits.values():
            self._points.append(self._get_all_segments_coords(digit))
        self._points = np.array(self._points).reshape(10, 16, 2)

    def _get_all_segments_coords(self, digit: Dict):
        all_digit_points = []
        # Take the segment that will be as { 'segment_0': [ points ]}
        for segment in digit.values():
            all_digit_points.append(segment)
        return np.array(all_digit_points)

    def animation(self) -> None:
        self._get_centered_coords()
        t           = np.linspace(0, 1, 20)
        length      = len(self._points)
        self._frames = []
        self._figure = plt.figure()
        print('# Frame generation started')
        for i in range(length):
            for t_i in t:
                intermediate_points = self._points[i] * (1 - t_i) + \
                       self._points[(i + 1) % length] * t_i
                digit_points = self._get_digit_coords(intermediate_points)
                # Shift them to the center
                digit_points[:, 0] += self._d_x
                digit_points[:, 1] += self._d_y
                self._draw_digit(digit_points.astype(np.int32))
            print(f'[{i}]')
        print('## Frame generation finished')

    def _get_digit_coords(self, intermediate_points):
        t      = np.linspace(0, 1, self._count)
        length = len(intermediate_points)
        coords = []
        for i in range(0, length - 3, self._p_count):
            for t_i in t:
                coords.append(
                              self._de_castlejau(
                                    intermediate_points[i:i + self._p_count],
                                    t_i,
                                    self._p_count
                                    )
                             )
        return np.array(coords).reshape(self._count * self._p_count, 2)

    def _de_castlejau(self, segment, t, n):
        # Algorithm De Castlejau to find the point to draw the line.
        for i in range(1, n):
            for j in range(0, n - i):
                segment[j] = (1 - t) * np.array(segment[j]) + \
                             t * np.array(segment[j + 1])
        return np.array(segment[0])

    def _draw_digit(self, digit_points):
        # Set the frame in color
        self._pixels = np.full((self._size, self._size, 3),
                              self._bg_color, dtype=np.uint8)
        for i in range(len(digit_points) - 1):
            # Call the method bresenham from class lab2
            super()._bresenham(digit_points[i][0],
                               digit_points[i][1],
                               digit_points[i + 1][0],
                               digit_points[i + 1][1])
        # Put the frame to the frames list
        temp_frame = plt.imshow(self._pixels)
        self._frames.append([temp_frame])


def main():
    filename           = 'digits.json'
    digits             = json.load(open(filename, 'r'))
    lab4               = Lab4(digits, 100, 4)
    lab4.size          = 1000
    lab4.bg_color      = [255, 255, 255]
    lab4.draw_color    = [255, 0, 0]
    lab4.animation()
    lab4.save_gif('digits.gif')


if __name__=='__main__':
    main()
