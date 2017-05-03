from musicvisualizer.pipeline.ir import VisualizableMixin
from numpy import zeros
import numpy as np
from math import sin, cos, atan, pi

class CircularOscillatorVisualizer(VisualizableMixin):
    def __init__(self, circular_oscillator, mode = 'dots'):
        self.cosc             = circular_oscillator
        self.mode             = mode
        self.number_of_points = circular_oscillator.number_of_points

    def _polar_2_cart(self, R, theta):
        # TODO: Inline this into visualize for better performance
        if R > 1.0:
            print ("R = {}, theta = {}".format(R, theta))
        width, height = self.width, self.height
        c_y,c_x = (height / 2, width / 2)

        # Anything more will potentially be off the screen
        maxR   = min(width, height) / 2.1
        x, y = maxR * R * cos(theta) + c_x, maxR*R * sin(theta) + c_y
        return y, x


    def visualize(self, width = 720, height = 512):
        '''Return a list of numpy frames'''
        self.width, self.height = width, height   # Store this for the _polar_2_cart
        pt_list  = list(iter(self.cosc))
        pt_width = len(pt_list[0])      # width of each points instance

        if pt_width > len(pt_list[0]):
            raise Exception('width of video must be greater than width of points')

        result   = []

        # Handle mode == 'dots
        if self.mode == 'dots':
            d_theta = pi / self.number_of_points
            for points in pt_list:
                theta   = 0.0
                arr = zeros(shape = (height, width, 3), dtype=np.uint8)
                for i, (point, vel) in enumerate(points):
                    # Weird offsets are to allow a 2x2 pixel (+/- 1...)
                    # HEY! So the following y value works like this:
                    #  -pi/2 <= arctan(x) <= pi/2, so dividing out by pi we get
                    # -1/2 <= arctan(x) / pi <= 1/2, and the result below is that
                    # we get a value between 0 and height

                    # XXX: This next bit will need to be adjusted!
                    # R ranges from -1.0 to 1.0
                    R = atan(5.0 * point) / (pi/2.0)
                    print("R =", R)
                    y,x = self._polar_2_cart(R, theta)
                    y,x = int(y), int(x)

                    if y >= height - 1:
                        y = height - 2
                    if y < 1:
                        y = 1
                    arr[y][x][0]     = 255
                    arr[y-1][x][0]   = 255
                    arr[y-2][x][0]   = 255
                    arr[y][x-1][0]   = 255
                    arr[y-1][x-1][0] = 255
                    arr[y-2][x-1][0] = 255
                    arr[y][x-2][0]   = 255
                    arr[y-1][x-2][0] = 255
                    arr[y-2][x-2][0] = 255

                    arr[y][x][1]     = 255
                    arr[y-1][x][1]   = 255
                    arr[y-2][x][1]   = 255
                    arr[y][x-1][1]   = 255
                    arr[y-1][x-1][1] = 255
                    arr[y-2][x-1][1] = 255
                    arr[y][x-2][1]   = 255
                    arr[y-1][x-2][1] = 255
                    arr[y-2][x-2][1] = 255

                    arr[y][x][2]     = 255
                    arr[y-1][x][2]   = 255
                    arr[y-2][x][2]   = 255
                    arr[y][x-1][2]   = 255
                    arr[y-1][x-1][2] = 255
                    arr[y-2][x-1][2] = 255
                    arr[y][x-2][2]   = 255
                    arr[y-1][x-2][2] = 255
                    arr[y-2][x-2][2] = 255
                    theta += d_theta


                result.append(arr)

        # Handle mode == 'bars'
        elif self.mode == 'bars':
            for points in pt_list:
                arr = zeros(shape = (height, width, 3), dtype=np.uint8)
                for i, (point, vel) in enumerate(points):
                    # Weird offsets are to allow a 2x2 pixel (+/- 1...)
                    x = int(i * (width-2) / pt_width + 2)
                    # HEY! So the following y value works like this:
                    #  -pi/2 <= arctan(x) <= pi/2, so dividing out by pi we get
                    # -1/2 <= arctan(x) / pi <= 1/2, and the result below is that
                    # we get a value between 0 and height
                    y = int( (height / 2) + atan(5.0 * point) * (height)/ (pi))
                    if y >= height - 1:
                        y = height - 2
                    if y < 1:
                        y = 1

                    mid = height / 2
                    if y > mid:
                        while y > mid:
                            arr[y][x][0]     = 255
                            arr[y][x-1][0]   = 255
                            arr[y][x-2][0]   = 255

                            arr[y][x][1]     = 255
                            arr[y][x-1][1]   = 255
                            arr[y][x-2][1]   = 255

                            arr[y][x][2]     = 255
                            arr[y][x-1][2]   = 255
                            arr[y][x-2][2]   = 255
                            y -= 1
                    else:
                        while y < mid:
                            arr[y][x][0]     = 255
                            arr[y][x-1][0]   = 255
                            arr[y][x-2][0]   = 255

                            arr[y][x][1]     = 255
                            arr[y][x-1][1]   = 255
                            arr[y][x-2][1]   = 255

                            arr[y][x][2]     = 255
                            arr[y][x-1][2]   = 255
                            arr[y][x-2][2]   = 255
                            y += 1
                result.append(arr)

        return result
        
    
