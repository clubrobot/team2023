from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])
PipeType = namedtuple('PipeType', ['parent', 'child'])
Command = namedtuple('Command', ['cmd', 'args'])
InitMsg = namedtuple(
    'InitMsg', ['refMarker', 'camera', 'mode', 'debug', 'dictionnary'])
