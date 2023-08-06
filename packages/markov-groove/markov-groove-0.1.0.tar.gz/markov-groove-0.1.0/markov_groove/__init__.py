"""
This framework allows for preprocessing audio files 
to make them usable in a machine learning context.
The markov_groove framework was created 
and written by Jan-Niclas de Vries.
"""

from .audio_file import *
from .onset_detector import *
from .sampler import *
from .sequencer import *
from .util import *

__version__ = "0.1"
