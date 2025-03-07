from typing import Iterable

from .color_condition import ColorCondition
from .extra_variable import ExtraVariable
from .utils import returnList, columnsToRows
from .column import Column


class ColorItem:
    def __init__(self, color=None, style=None):
        self.color = color
        self.style = style


def transposeMatrix(matrix):
    return columnsToRows(matrix)

class ConditionedMatrixBuilder:
    def __init__(self):
        self.matrix: list[Column] = None
        self.condition: ColorCondition = None

    def setMatrix(self, matrix):
        self.matrix = matrix
        return self
    
    def setCondition(self, condition):
        self.condition = condition
        return self

    @returnList
    def _createBoolColumn(self, array):
        extra = ExtraVariable()

        if self.condition.initMethod:
            self.condition.initMethod(array, extra)
            
        for index, item in enumerate(array):
            args = [locals()[argName] for argName in self.condition.args]

            yield self.condition.method(*args)

    @returnList
    def _createBoolMatrix(self):
        for column in self.matrix:
            yield self._createBoolColumn(column)


    def build(self):
        if self.condition.type == 'row':
            self.matrix = transposeMatrix(self.matrix)
            self.matrix = self._createBoolMatrix()
            self.matrix = transposeMatrix(self.matrix)

        if self.condition.type == 'column':
            self.matrix = self._createBoolMatrix()

        return self.matrix

class MatricesOverlayExecutor:
    def __init__(self, emptyItem, columnsAmount, columnSize, matrices: list[list[Column]]):
        self.emptyItem = emptyItem
        self.columnsAmount = columnsAmount
        self.columnSize = columnSize
        self.matrices = matrices

    @returnList
    def overlayForColumn(self, columnIndex):
        for itemIndex in range(self.columnSize):
            currentItem = self.emptyItem

            for matrix in self.matrices:
                currentItem = matrix[columnIndex][itemIndex]

                if currentItem != self.emptyItem:
                    break
            
            yield currentItem

    @returnList
    def overlayForMatrix(self):
        for columnIndex in range(self.columnsAmount):
            yield self.overlayForColumn(columnIndex)



class Painter:
    def __init__(self, colorConditions: Iterable[ColorCondition]=None, emptyItem=None):
        self.columnsAmount = None
        self.columnSize = None
        self.matrix = None
        self.contentMatrix = None

        self.colorConditions = colorConditions if colorConditions else list()  
        self.emptyItem = emptyItem

    @returnList
    def _columnObjectsToLists(self, columns: list[Column]):
        for column in columns:
            yield column.items

    @returnList
    def _createContentMatrix(self):
        for column in self.matrix:
            yield [item.content.strip() for item in column]

    @returnList
    def _createConditionedMatrices(self):
        for condition in self.colorConditions:
            yield ConditionedMatrixBuilder().setMatrix(self.contentMatrix).setCondition(condition).build()


    @returnList
    def _fillBoolMatrix(self, boolMatrix, valueForTrue, valueForFalse):
        for column in boolMatrix:
            yield [valueForTrue if TrueOrFalse else valueForFalse for TrueOrFalse in column]

    def _createStyleMask(self, boolMatrix, condition: ColorCondition):
        return self._fillBoolMatrix(boolMatrix, condition.style, self.emptyItem)
    
    def _createColorMask(self, boolMatrix, condition: ColorCondition):
        return self._fillBoolMatrix(boolMatrix, condition.color, self.emptyItem) 




    def _applyMask(self, mask, applyMethod):
        for i in range(self.columnsAmount):
            for j in range(self.columnSize):
                applyMethod(self.matrix[i][j], mask[i][j])

    def _applyColorMask(self, mask):
        def applyMethod(columnItem, color):
            columnItem.color = color

        return self._applyMask(mask, applyMethod)

    def _applyStyleMask(self, mask):
        def applyMethod(columnItem, style):
            columnItem.style = style

        return self._applyMask(mask, applyMethod)

    def addColorCondition(self, colorCondition):
        self.colorConditions.append(colorCondition)

    def paint(self, matrix, columnsAmount, columnSize):
        self.columnsAmount = columnsAmount
        self.columnSize = columnSize

        self.matrix = self._columnObjectsToLists(matrix)
        self.contentMatrix = self._createContentMatrix()

        conditionedMatrices = self._createConditionedMatrices()

        styleMasks = [self._createStyleMask(conditionedMatrix, condition) for conditionedMatrix, condition in zip(conditionedMatrices, self.colorConditions)]
        colorMasks = [self._createColorMask(conditionedMatrix, condition) for conditionedMatrix, condition in zip(conditionedMatrices, self.colorConditions)]

        mergedStyleMask = MatricesOverlayExecutor(self.emptyItem, self.columnsAmount, self.columnSize, styleMasks).overlayForMatrix()
        mergedColorMask = MatricesOverlayExecutor(self.emptyItem, self.columnsAmount, self.columnSize, colorMasks).overlayForMatrix()

        self._applyColorMask(mergedColorMask)
        self._applyStyleMask(mergedStyleMask)