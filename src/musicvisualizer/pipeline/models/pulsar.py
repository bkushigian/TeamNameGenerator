'''
circular_oscillator.py: defines a ModelledRepr extension that begins with a
discretized circle (i.e., n points) about the screen and is perturbed by pushing
the points up and down. This draws heavily on the LinearOscillatorModel. Each
point is connected to its neighbors by rubber band and to its inital position by
some other band. Thus at each point in time a point is acted upon by force

        F = F_l + F_r + F_b

where F_l is the force acted upon it by
_______________________________________________________________ LINE
._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._. DISCRETIZED LINE

This will be the test case for the initial extension of ModelledRepr. We will
update/expand/tweak ModelledRepr based on this implementation to make further
extensions easier.
'''

from musicvisualizer.pipeline.ir import ModelledRepr, PhaseVocPR
from musicvisualizer.pipeline.models.linear_oscillator import LinearOscillatorModel
import numpy as np
from numpy import ndarray, full, zeros
from math import sin, cos, sqrt, atan, pi

# Don't know what we'll need...
from itertools import count, cycle, repeat

class PulsarMR(LinearOscillatorModel):
    # TODO: include params for ModelledRepr

    def __init__(self, 
                 pir,                      # A Parametric Representation
                 input_fields,             # Parameters
                 sampleRate       = 24, 
                 sampleRange      = (None, None),
                 dataIn           = None, 
                 dataInFPS        = 48,
                 parameters       = None, 
                 number_of_points = 512,
                 hook             = 121.0,
                 vertical_hook    = 0.2,
                 data_shape       = (256,),
                 damping          = 0.95):

        super(PulsarMR, self).__init__(
                 pir, 
                 input_fields,
                 sampleRate, 
                 sampleRange, 
                 dataIn, 
                 dataInFPS, 
                 parameters, 
                 number_of_points, 
                 hook, 
                 vertical_hook, 
                 data_shape, 
                 damping)


    def __str__(self):
        return "<PulsarModel>"

    def __repr__(self):
        return str(self)
