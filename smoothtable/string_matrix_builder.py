from .constants import EMPTY

class StringMatrixBuilder:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
        self._rows = [[EMPTY for _ in range(self._width)] for _ in range(self._height)]

        self._currentString = EMPTY

    def _setItem(self, string, x, y):
        self._rows[y][x] = string

    def _joinRow(self, row):
        return EMPTY.join(row)

    def set(self, string):
        self._currentString = string
        return self
    
    def at(self, y, x):
        self._setItem(self._currentString, x, y)
        return self
    
    def buildVerticalList(self):
        return [EMPTY.join(row) for row in self._rows]

    def buildHorizontalList(self):
        return [EMPTY.join(self._rows[rowIndex][columnIndex] for rowIndex in range(self._height)) for columnIndex in range(self._width)]