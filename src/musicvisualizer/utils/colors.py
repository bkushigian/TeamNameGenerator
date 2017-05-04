from math import sin, cos, pi
import numpy as np
from numpy import uint8

def rotate(l, n):
    '''rotate list l by n'''
    return l[n:] + l[:n]

class ColorWheel(object):
    ''' A convenience function for creating/parametrizing colors '''
    def __init__(self, size = 256, red = True, green = True, blue = True):
        self.size = size
        self.dt          = 2*pi / size
        self.R, self.G, self.B = red, green, blue

        colors = sum([red, green, blue])  # How many colors do we have?
        spread = size // 2                # Spread to side from peak
        if colors:
            spread = size // (colors)
        else:
            raise Exception("Color wheel with no colors is dumb. Stop it")
        dc     = 255 / spread   # The color delta
        decr   = [uint8(255 - int(i * dc)) for i in range(spread)]
        incr   = decr[::-1]
        filler = [uint8(0) for i in range(size - 2*len(incr))]
        cdist  = decr + filler + incr
        zdist  = [uint8(0) for i in range(size)]
        # Build it!
        if colors == 0:  # Dumb, what do we do?
            pass
        elif colors == 1:

            if red:
                pR = rotate(cdist, 0)
            else:
                pR = zdist
            if green:
                pG = rotate(cdist, 0)
            else:
                pG = zdist
            if blue:
                pB = rotate(cdist, 0)
            else:
                pB = zdist
        elif colors == 2:
            colorseen = 0
            if red:
                pR = rotate(cdist, 0)
                colorseen += 1
            else:
                pR = zdist

            if green:
                pG = rotate(cdist, int(colorseen * size / 3))
                colorseen += 1
            else:
                pG = zdist

            if blue:
                pB = rotate(cdist, int(colorseen * size / 3))
            else:
                pB = zdist

        elif colors == 3:
            pR = rotate(cdist, 0)
            pG = rotate(cdist, size // 3)
            pB = rotate(cdist, -1 * size // 3)
        self.colors = list(zip(pR, pG, pB))


    def __call__(self, i, damp = 1.0):
        i = i % self.size
        if damp <= 0.0:
            return (0,0,0)
        if damp < 1.0:
            return tuple(map(lambda x : uint8(x*damp), self.colors[i]))
        return self.colors[i]


