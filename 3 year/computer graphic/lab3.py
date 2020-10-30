from lab2 import np, plt, Lab2, get_file_data, get_points_and_edges
import matplotlib.animation as anim
from matplotlib.animation import PillowWriter


class Lab3(Lab2):
    """Class to implement an animation of the teapot.
       it inheritances from lab2, so we can easily draw teapot now
    """
    def __init__(self, points, edges):
        # Call the super constructor
        super().__init__(points, edges)

    def animation(self, frames_count) -> None:
        self.get_scalable_points()
        self.frames_count = frames_count
        zone = self.frames_count // 2
        # Get the shift matrix
        self.T = self._shift_matrix()
        # Transposition
        x = self.points.T
        # Cast to projective coordinates
        self.proj_x = self._to_proj_coords(x)
        # Linspace to reduce the size of teapot
        reduce = np.linspace(2, 1, zone)
        # Linspace to increase the size of teapot
        increase = np.linspace(1, 2, zone)
        # coefficients to
        self.coefficients  = np.concatenate((increase, reduce))
        self.frames = []
        # Linspace from read color to green color in pixels
        r_to_g = np.array(np.linspace(255, 0, zone, dtype=np.int32))
        # Linspace from green color to red color in pixels
        g_to_r = np.array(np.linspace(0, 255, zone, dtype=np.int32))
        # Get the various forms of color in pixels
        self.color = np.array(np.concatenate((np.concatenate((r_to_g, g_to_r)).reshape(-1, 1),
                                         np.concatenate((g_to_r, r_to_g)).reshape(-1, 1),
                                         np.zeros(frames_count).reshape(-1, 1)), axis=1))
        self.figure = plt.figure()
        print('# Frame generation started')
        for frame in range(self.frames_count):
            self._generate_one_frame(frame)
        print('## Frame generation finished')

    def _shift_matrix(self):
        # Center shift matrix
        center = -self.center
        shift = np.array([[1, 0, center[0]], [0, 1, center[1]], [0, 0, 1]])
        return shift

    def _to_proj_coords(self, x):
        _, c = x.shape
        proj_x = np.concatenate([x, np.ones((1, c))], axis = 0)
        return proj_x

    def _generate_one_frame(self, frame) -> None:
        # Calculate the angle of rotation
        angle = frame * 4 * np.pi / self.frames_count
        # Calculate the diagonal matrix from coefficient
        A = self._diag_matrix(self.coefficients[frame])
        # Calculate the rotate matrix from angle
        R = self._rot_matrix(angle)
        # X' = T^(-1) * A * R * T * X
        new_proj_x = np.linalg.inv(self.T) @ A @ R @ self.T @ self.proj_x
        # Cast to cartesian coordinates
        new_x = self._to_cart_coords(new_proj_x)
        self.points = np.int32(np.round(new_x.T))
        self.draw_color = self.color[frame]
        self.draw_teapot()
        # Get frame
        temp_frame = plt.imshow(self.pixels)
        # Put the frame to the frames list
        self.frames.append([temp_frame])
        print(f'[{frame + 1}]')

    def _diag_matrix(self, coef):
        diagonal = np.array([[coef, 0, 0],[0, coef, 0], [0, 0, 1]])
        return diagonal

    def _rot_matrix(self, angle):
        rot = np.array([[np.cos(angle), -np.sin(angle), 0],
                        [np.sin(angle), np.cos(angle), 0],
                        [0, 0, 1]])
        return rot

    def _to_cart_coords(self, new_proj_x):
        new_proj_x = new_proj_x[:-1] / new_proj_x[-1]
        return new_proj_x

    def save_gif(self, filename) -> None:
        plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg.exe'
        print('### Saving in ' + filename)
        animation = anim.ArtistAnimation(self.figure, self.frames, interval=40,
                                         blit=True, repeat_delay=0)
        writer = PillowWriter(fps=24)
        animation.save(filename, writer=writer)
        print('#### Saved!')
        plt.show()


def main():
    filename           = 'teapot.obj'
    data               = get_file_data(filename)
    points, edges      = get_points_and_edges(data)
    lab3 = Lab3(points, edges)
    lab3.scale         = 150
    lab3.size          = 2500
    lab3.bg_color      = [255, 255, 255]
    lab3.draw_color    = [255, 0, 0]
    lab3.animation(100)
    lab3.save_gif('teapot.gif')


if __name__=="__main__":
    main()
