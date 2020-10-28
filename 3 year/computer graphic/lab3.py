from lab2 import np, plt, Lab2, get_file_data, get_points_and_edges


class Lab3(Lab2):
    """Class to implement an animation of the teapot.
       it inheritances from lab2, so we can easily draw teapot now
    """
    def __init__(self, points, edges):
        # Call the super constructor
        super().__init__(points, edges)


def main():
    filename           = 'teapot.obj'
    data               = get_file_data(filename)
    points, edges      = get_points_and_edges(data)
    lab3 = Lab3(points, edges)
    lab3.scale         = 300
    lab3.size          = 2500
    lab3.bg_color      = [255, 255, 255]
    lab3.draw_color    = [255, 0, 0]
    lab3.draw_teapot()


if __name__=="__main__":
    main()
