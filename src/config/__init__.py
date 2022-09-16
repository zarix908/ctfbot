import os

from .config import load

filename = './notprovide/devconfig.ini' if os.getenv('TEST') == '1' else './notprovide/prodconfig.ini'
config = load(filename)
