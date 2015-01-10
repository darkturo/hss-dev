__version__ = '0.0.2'
__description__ = """ HSS development and testing toolbox for craftmen and superheroes """

import dtool
from exceptions import CommandLineError, CommandLineMisspelledError, ExitWithSuccessException, ExitWithErrorException

__all__ = [
            'dtool',
            'CommandLineError',
            'CommandLineMisspelledError', 
            'ExitWithSuccessException',
            'ExitWithErrorException'
          ]
