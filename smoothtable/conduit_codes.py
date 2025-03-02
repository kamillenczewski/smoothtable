from .constants import (
    BOTTOM_RIGHT_CORNER, BOTTOM_LEFT_CORNER, TOP_RIGHT_CORNER, TOP_LEFT_CORNER,
    RIGHT_CONDUIT, LEFT_CONDUIT, BOTTOM_CENTER_CONDUIT, TOP_CENTER_CONDUIT, CENTER_CONDUIT
)

"""
Conduit code determines whether 
a point in specific direction has connection 
with the center point or not.

UP DOWN LEFT RIGHT

1100 -> vertical
1010 -> bottom right corner
1001 -> bottom left corner
0110 -> top right corner
0101 -> top left corner
0011 -> horizontal

1110 -> right conduit
1101 -> left conduit
1011 -> bottom center conduit
0111 -> top center conduit

1111 -> center conduit
"""

CONDUIT_CODES_AND_CONDUITS = {
    '1010': BOTTOM_RIGHT_CORNER,
    '1001': BOTTOM_LEFT_CORNER,
    '0110': TOP_RIGHT_CORNER,
    '0101': TOP_LEFT_CORNER,
    '1110': RIGHT_CONDUIT,
    '1101': LEFT_CONDUIT,
    '1011': BOTTOM_CENTER_CONDUIT,
    '0111': TOP_CENTER_CONDUIT,
    '1111': CENTER_CONDUIT
}