from typing import Iterable

from .color_condition import ColorCondition
from .extra_variable import ExtraVariable
from .utils import rowsToColumns, returnList, columnsToRows
from .constants import COLORS, TEXT_STYLES


EMPTY_MASK_ITEM = None


class ColorItem:
    def __init__(self, color=None, style=None):
        self.color = color
        self.style = style


def paintString(string, color, style):
    color = COLORS[color] if color else ""
    style = TEXT_STYLES[style] if style else ""

    string = color + style + "{}\033[0m".format(string)

    return string



class MaskMerger:
    @classmethod
    def mergeColumnMasks(cls, masks, columnIndex, columnSize):
        for itemIndex in range(columnSize):
            maskItem = EMPTY_MASK_ITEM

            for mask in masks:
                maskItem = mask[columnIndex][itemIndex]

                if maskItem != EMPTY_MASK_ITEM:
                    break
            
            yield maskItem

    @classmethod
    def mergeMasks(cls, masks, columnsAmount, columnSize):
        for columnIndex in range(columnsAmount):
            yield cls.mergeColumnMasks(masks, columnIndex, columnSize)


class ColorMaskCreator:
    @classmethod
    @returnList
    def createColumnMask(cls, condition, array):
        extra = ExtraVariable()

        if condition.initMethod:
            condition.initMethod(array, extra)
            
        for index, item in enumerate(array):
            args = [locals()[argName] for argName in condition.args]

            if condition.method(*args):
                yield ColorItem(condition.color, condition.style)
            else:
                yield EMPTY_MASK_ITEM

    @classmethod
    @returnList
    def createMask(cls, condition, columns):
        for column in columns:
            yield cls.createColumnMask(condition, column)

    @classmethod
    @returnList
    def createMasks(cls, arrays, conditions):
        for condition in conditions:
            if condition.type == 'row':
                rows = columnsToRows(arrays)
                mask = cls.createMask(condition, rows)
                mask = rowsToColumns(mask)
                yield mask
            
            if condition.type == 'column':
                yield cls.createMask(condition, arrays)

class Painter:
    def __init__(self, colorConditions: Iterable[ColorCondition]):
        self.colorConditions = colorConditions        


    def createMask(self, columns, columnsAmount, columnSize):
        masks = ColorMaskCreator.createMasks(columns, self.colorConditions)
        finalMask = MaskMerger.mergeMasks(masks, columnsAmount, columnSize)
        return finalMask

    @returnList
    def applyMaskToColumn(self, column, columnMask):
        for stringItem, colorItem in zip(column, columnMask):
            if colorItem:
                yield paintString(stringItem, colorItem.color, colorItem.style)
            else:
                yield stringItem

    @returnList
    def applyMask(self, columns, mask):
        for column, columnMask in zip(columns, mask):
            yield self.applyMaskToColumn(column, columnMask)

    def paint(self, columns):
        columnsAmount = len(columns)
        columnSize = len(columns[0])
        mergedMask = self.createMask(columns, columnsAmount, columnSize)
        columns = self.applyMask(columns, mergedMask)
        return columns