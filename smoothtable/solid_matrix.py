from typing import Iterable

from .utils import returnList
from .extra_variable import ExtraVariable


class SolidMatrix:
    def __init__(self, defaultValue, itemsType=None, width=None, height=None, arrays=None):
        self.defaultValue = defaultValue
        self.itemsType = itemsType

        self.height, self.width = self._normalizeHeightAndWidth(width, height)
        self._validateHeightAndWidth(width, height)

        if arrays:
            self._validateArrays(arrays)

            self.arrays = arrays
            self.height = len(arrays[0])
            self.width = len(arrays)
        elif width and height:
            self.arrays = [[self.defaultValue for _ in range(self.height)] for _ in range(self.width)]
        else:
            raise ValueError('There is no passed arguments which the matrix can build be build of!')

    def _validateArrays(self, arrays):
        if arrays:
            length = len(arrays[0])

        for array in arrays:
            if not isinstance(array, Iterable):
                raise ValueError('Row must be Iterable!')
            
            if len(array) != length:
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
        if self.itemsType and not isinstance(item, self.itemsType):
                raise ValueError(f"matrix's item should have type: {self.itemsType}!")
            
        return True



    def getItem(self, x, y):
        self._validateCoordinates(x, y)
        return self.arrays[y][x]
    
    def setItem(self, x, y, item):
        self._validateCoordinates(x, y)
        self._validateItem(item)
        self.arrays[y][x] = item

    def __str__(self):
        return '\n' + '\n'.join(''.join(map(str, array)) for array in self.arrays) + '\n'

    @returnList
    def convert(self, convertMethod):
        for array in self.arrays:
            yield [convertMethod(item) for item in array]

    def forEach(self, forEachMethod):
        for array in self.arrays:
            for item in array:
                forEachMethod(item)

    def fullFor(self, method):
        extra = ExtraVariable()

        for array in self.arrays:
            for index, item in enumerate(array):
                method(extra, array, index, item)