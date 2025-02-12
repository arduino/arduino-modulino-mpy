__version__ = '1.0.0'
__author__ = "Sebastian Romero"
__license__ = "MPL 2.0"
__maintainer__ = "Arduino"

# Import core classes and/or functions to expose them at the package level
from .helpers import map_value, map_value_int
from .modulino import Modulino
from .pixels import ModulinoPixels, ModulinoColor
from .thermo import ModulinoThermo
from .buzzer import ModulinoBuzzer
from .buttons import ModulinoButtons
from .knob import ModulinoKnob
from .movement import ModulinoMovement
from .distance import ModulinoDistance