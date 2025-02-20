from .constants import *
from .concat_utils import bottomConcat

"""
Layers = [
    {'1-3': 'Identification', 'Other':'4-5'},
    {'1-1': 'Id', '2-2': 'First name', '3-3': 'Second Name', '4-4':'Favourite Color', '5-5': 'Owned Car'}
]
"""

"""
Line types:
 - top
 - content
 - conduit
 - bottom
"""

"""
╭─────────────────┬───────────────────╮ <-- TOP
│ Favourite Color │ AHA               │ <-- CONTENT
├─────────────────┴───────────────────┤    ╭─────────────────╮    ╭─────╮ <-- CONDUIT, TOP, TOP
│ Identification                      │    │ Favourite Color │    │ AHA │ <-- CONTENT, CONTENT, CONTENT
├───┬───────────┬────────────┬────────┼────┼───────┬────┬────┼────┼─────┤ <-- BOTTOM, BOTTOM, BOTTOM
"""


"""
╭─────────────────┬───────────────────╮
│ Favourite Color │ AHA               │
├─────────────────┼───────────────────┤ 
│ Favourite Color │ AHA               │
├─────────────────┴───────────────────┤    ╭─────────────────╮    ╭─────╮
│ Identification                      │    │ Favourite Color │    │ AHA │
├───┬───────────┬────────────┬────────┼────┼───────┬────┬────┼────┼─────┤
│ 1 │ Kamil     │ Lenczewski │ Blue   │ R1 │ R1    │ R1 │ R1 │ R1 │ R1  │
│ 2 │ Anastazja │ Kasprzyk   │ Red    │ R1 │ R1    │ R1 │ R1 │ R1 │ R1  │
│ 3 │ Karolina  │ Olawska    │ Yellow │ V1 │ V1    │ V1 │ V1 │ V1 │ V1  │
╰───┴───────────┴────────────┴────────┴────┴───────┴────┴────┴────┴─────╯
"""

class LabelsLayer:
    def __init__(self, names, ranges):
        self.names = names 
        self.ranges = ranges # ranges connected to lower layers
        # add lengths here
        # becuase why not
        # it will be better visible and readable

def constructTopLine(lowerLayerLengths, startChar=None, endChar=None):
    startChar = startChar if startChar else TOP_LEFT_CORNER
    endChar = endChar if endChar else TOP_RIGHT_CORNER

    return startChar + TOP_CENTER_CONDUIT.join(length * HORIZONTAL_LINE for length in lowerLayerLengths) + endChar

def constructContentLine(names, startChar=None, endChar=None):
    startChar = startChar if startChar else LEFT_VERTICAL_LINE
    endChar = endChar if endChar else RIGHT_VERTICAL_LINE

    return startChar + CENTER_VERTICAL_LINE.join(names) + endChar

def constructConduitLine(layerLengths, startChar=None, endChar=None):
    startChar = startChar if startChar else LEFT_CONDUIT
    endChar = endChar if endChar else RIGHT_CONDUIT

    return startChar + BOTTOM_CENTER_CONDUIT.join(length * HORIZONTAL_LINE for length in layerLengths) + endChar



def constructLayer(layer: LabelsLayer):
    lengths = list(map(len, layer.names))

    return NEW_LINE.join([
        constructTopLine(lengths),
        constructContentLine(layer.names),
        constructConduitLine(lengths)
    ])

def constructLayers(layers: list[LabelsLayer]):
    pass

def main():
    layer = LabelsLayer(
        names=['Name', 'id', 'your mom'],
        ranges=[(0,0), (1,1), (2,2)]
    )
    result = constructLayer(layer)

    print(result)
