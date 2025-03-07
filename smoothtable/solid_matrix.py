from typing import Iterable

from .utils import returnList
from .extra_variable import ExtraVariable


class SolidMatrix:
    def __init__(self, defaultValue, type=None, width=None, height=None, rows=None):
        self.type = type
        self.height, self.width = self._normalizeHeightAndWidth(width, height)
        self._validateHeightAndWidth(width, height)

        self.defaultValue = defaultValue

        if rows:
            self._validateRows(rows)

            self.rows = rows
            self.height = len(rows)
            self.width = len(rows[0])
        elif width and height:
            self.rows = [[self.defaultValue for _ in range(width)] for _ in range(height)]
        else:
            raise ValueError('There is no passed arguments which the matrix can build be build of!')

    def _validateRows(self, rows):
        if rows:
            length = len(rows[0])

        for row in rows:
            if not isinstance(row, Iterable):
                raise ValueError('Row must be Iterable!')
            
            if len(row) != length:
                raise ValueError('Length of all rows should be the same!')
            
    @staticmethod
    def _normalizeHeightAndWidth(height, width):
        if height and not width:
            width = 1

        if width and not height:
            height = 1

        return height, width

    @staticmethod
    def _validateHeightAndWidth(height, width):
        if not height and not width:
            return

        if not isinstance(height, int):
            raise ValueError("Variable 'height' has incorrect type! 'int' is needed!")

        if not isinstance(width, int):
            raise ValueError("Variable 'width' has incorrect type! 'int' is needed!")    

        if height <= 0:
            raise ValueError("'height' must be positive!")
        
        if width <= 0:
            raise ValueError("'width' must be positive!")

    def _validateCoordinates(self, x, y):
        if not 0 <= x < self.width:
            raise ValueError(f'x coordinate should be in range [0, {self.width})!')

        if not 0 <= y < self.height:
            raise ValueError(f'y coordinate should be in range [0, {self.height})!')

    def _validateItem(self, item):
        if self.type and not isinstance(item, self.type):
                raise ValueError(f"matrix's item should have type: {self.type}!")
            
        return True

    def getItem(self, x, y):
        self._validateCoordinates(x, y)
        return self.rows[y][x]
    
    def setItem(self, x, y, item):
        self._validateCoordinates(x, y)
        self._validateItem(item)
        self.rows[y][x] = item

    def __str__(self):
        return '\n' + '\n'.join(''.join(map(str, row)) for row in self.rows) + '\n'

    @returnList
    def convert(self, convertMethod):
        for row in self.rows:
            yield [convertMethod(item) for item in row]

    def forEach(self, forEachMethod):
        for row in self.rows:
            for item in row:
                forEachMethod(item)

    def fullFor(self, method):
        extra = ExtraVariable()

        for row in self.rows:
            for index, item in enumerate(row):
                method(extra, row, index, item)