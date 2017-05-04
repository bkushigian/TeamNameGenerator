'''
pipeline.py
define the Pipeline class
Date:   4/4/17
Author: Benjamin Kushigian

'''

from musicvisualizer.pipeline.mp3_to_wav import mp3_to_wav
from aubio import source
from moviepy.editor import *

class Pipeline(object):
    def __init__(self, input_fields):
        self.input_fields = input_fields
        self.extract_inputs()
        self.convert_file()     # change source from mp3 to wav
        # XXX: For now, just build the video!

    def extract_inputs(self):
        '''This extracts inputs from the input_fields to member variables'''

        # First we set defaults

        self.visualization = 'linear-oscillator'
        self.verbose       = False
        self.output        = 'output.mp4'
        self.groovy        = 0.0

        params = self.input_fields

        # Now extract any data that could be useful
        if 'visualization' in params:
            self.visualization = params['visualization']
        if 'verbose' in params and params['verbose']:
            self.verbose = True
        if 'output' in params:
            self.output = params['output']
        if 'groovy' in params:
            self.groovy = params['groovy']

    def convert_file(self):
        ''' takes a filepath source and returns a new source in temp dir as a wav'''
        self.source      = self.input_fields['source']
        self.source_wav = mp3_to_wav(self.source)

    def buildVisualization(self):
        # XXX Assuming that we are doing a linear oscillator
        # Need to store a field in InputFields for type of visualization
        # later if we want multiple types of visualizations
        if self.visualization == 'linear-oscillator':
            visualizer = self.buildLinearOscillatorVisualizer()
        elif self.visualization == 'circular-oscillator':
            visualizer = self.buildCircularOscillatorVisualizer()
        elif self.visualization == 'pulsar':
            visualizer = self.buildPulsarVisualizer()
        else:
            if self.verbose:
                print('Warning: no visualization {}'.format(self.visualization))
                print('Default visualization: linear-oscillator')
            visualizer = self.buildLinearOscillatorVisualizer()

        self.makeMovie(visualizer)



    def makeMovie(self, visualizer):
        output = self.output
        frames = visualizer.visualize()
        clip   = ImageSequenceClip(frames, fps = 24)

        if self.verbose:
            print('Pipeline.makeMovie()')
            print('    output = {}'.format(output))

        try:
            clip.write_videofile(output, fps = 24, audio=self.source)
        except:
            try:
                clip.write_videofile(output, fps = 24, audio=self.source_wav)
            except:
                print("[!] ERROR: Couldn't include audio into", output)
                clip.write_videofile(output, fps = 24)

    def buildLinearOscillatorVisualizer(self):
        from musicvisualizer.pipeline.ir import PhaseVocPR, AudioRepr
        from musicvisualizer.pipeline.models.linear_oscillator import LinearOscillatorModel
        from musicvisualizer.pipeline.models.linear_oscillator_visualizer import LinearOscillatorVisualizer
        
        if self.verbose:
            print("Creating AIR")
        audio = AudioRepr(self.source_wav, self.input_fields)

        if self.verbose:
            print("Creating PIR")
        phvoc = PhaseVocPR(audio, self.input_fields)
        if self.verbose:
            print("Creating MIR")
        dataInFPS = phvoc.dataInFPS # XXX: This should be automatic
        linos = LinearOscillatorModel(
                phvoc,                         # Phase Vocoder
                input_fields     = self.input_fields,
                sampleRate       = 24,         # Visual sample rate
                dataInFPS        = dataInFPS,  # Data sample rate (to generate visual)
                number_of_points = 256,        # how many points in simulation?
                hook             = 821.0,
                vertical_hook    = .15,
                data_shape       = (256, ),
                damping          = 0.92)
        if self.verbose:
            print("Creating VIR")
        lovis = LinearOscillatorVisualizer(linos, mode = 'dots')
        return lovis

    def buildCircularOscillatorVisualizer(self):
        from musicvisualizer.pipeline.ir import PhaseVocPR, AudioRepr
        from musicvisualizer.pipeline.models.circular_oscillator import CircularOscillatorMR
        from musicvisualizer.pipeline.models.circular_oscillator_visualizer import CircularOscillatorVisualizer
        
        if self.verbose:
            print("Creating AIR")
        audio = AudioRepr(self.source_wav, self.input_fields)

        if self.verbose:
            print("Creating PIR")
        phvoc = PhaseVocPR(audio, self.input_fields)
        if self.verbose:
            print("Creating MIR")
        dataInFPS = phvoc.dataInFPS # XXX: This should be automatic
        circosc = CircularOscillatorMR(
                  phvoc,                         # Phase Vocoder
                  input_fields     = self.input_fields,
                  sampleRate       = 24,         # Visual sample rate
                  dataInFPS        = dataInFPS,  # Data sample rate (to generate visual)
                  number_of_points = 256,        # how many points in simulation?
                  hook             = 821.0,
                  vertical_hook    = .15,
                  data_shape       = (256, ),
                  damping          = 0.92)
        if self.verbose:
            print("Creating VIR")
        cvis = CircularOscillatorVisualizer(circosc, mode = 'dots')
        return cvis

    def buildPulsarVisualizer(self):
        from musicvisualizer.pipeline.ir import PhaseVocPR, AudioRepr
        from musicvisualizer.pipeline.models.pulsar import PulsarMR
        from musicvisualizer.pipeline.models.pulsar_visualizer import PulsarVisualizer
        
        if self.verbose:
            print("Creating AIR")
        audio = AudioRepr(self.source_wav, self.input_fields)

        if self.verbose:
            print("Creating PIR")
        phvoc = PhaseVocPR(audio, self.input_fields)
        if self.verbose:
            print("Creating MIR")
        dataInFPS = phvoc.dataInFPS # XXX: This should be automatic
        circosc = PulsarMR(
                  phvoc,                         # Phase Vocoder
                  input_fields     = self.input_fields,
                  sampleRate       = 24,         # Visual sample rate
                  dataInFPS        = dataInFPS,  # Data sample rate (to generate visual)
                  number_of_points = 256,        # how many points in simulation?
                  hook             = 821.0,
                  vertical_hook    = .15,
                  data_shape       = (256, ),
                  damping          = 0.92)
        if self.verbose:
            print("Creating VIR")
        cvis = PulsarVisualizer(circosc, mode = 'dots')
        return cvis
