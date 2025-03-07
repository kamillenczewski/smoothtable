from typing import Iterable

from .cells_with_conduits_builder import CellsWithConduitsBuilder
from .utils import isConduit, returnList
from .conduit_codes import CONDUIT_CODES_AND_CONDUITS
from .cell import Cell
from .empty_cell import EmptyCell
from .column import Column
from .constants import HORIZONTAL_LINE, CONDUIT_SYMBOL, VERTICAL_LINE, SPACE
from .extendable_matrix import ExtendableMatrix
from .column_item import ColumnItem
from .string_color_and_style import getColor, getStyle, RESET_STR_FORMAT_TAG


def stringToChars(string):
    return [char for char in string]

def stringListToMatrix(strings):
    return ExtendableMatrix(
        defaultValue=SPACE, 
        rows=[stringToChars(string) for string in strings]
    )

def stringsMatrixToExtendableMatrix(stringsMatrix: list[list[str]]):
    return ExtendableMatrix(
        defaultValue=SPACE, 
        rows=stringsMatrix
    )


class CellsBuilder:
    def __init__(self):
        self.builder = CellsWithConduitsBuilder(isConduit, CONDUIT_CODES_AND_CONDUITS)
    
    def _validateColumns(self, columns):
        if not isinstance(columns, Iterable):
            raise ValueError('Columns should be Iterable!')
        
        for column in columns:
            if not isinstance(column, Column):
                raise ValueError('Each column should be type of Column!')

    def _validateRows(self, rows):
        if not isinstance(rows, Iterable):
            raise ValueError('Rows should be Iterable!')
        
        for row in rows:
            if not isinstance(row, Iterable):
                raise ValueError('Each row should be Iterable!')
            
            for cell in row:
                if not isinstance(cell, Cell) and not isinstance(cell, EmptyCell):
                    raise ValueError('Each row cell should be type of Cell or EmptyCell!')

    def appendColumns(self, columns: Iterable[Column]):
        self._validateColumns(columns)

        self.builder.withConstructMethod(self._columnConstructMethod)

        for column in columns:
            self.builder.append(column)
            self.builder.increaseCurrentX(column.length + 1)

        return self

    def appendRows(self, rows: Iterable[Iterable[Cell | EmptyCell]]):
        self._validateRows(rows)

        self.builder.withConstructMethod(self._cellConstructMethod)

        startX = self.builder.getCurrentX()

        for row in rows:
            for rowCell in row:
                self.builder.append(rowCell)
                self.builder.increaseCurrentX(rowCell.length - 1)
            
            self.builder.increaseCurrentY(2)
            self.builder.setCurrentX(startX)
        
        return self

    def build(self):
        return self.builder.build()

    def _columnConstructMethod(self, column: Column):
        topLine = bottomLine = [CONDUIT_SYMBOL] + column.length * [HORIZONTAL_LINE] + [CONDUIT_SYMBOL]
        middleLines = self._createColumnMiddleLines(column)

        # topLine = CONDUIT_SYMBOL + column.length * HORIZONTAL_LINE + CONDUIT_SYMBOL
        # middleLines = [VERTICAL_LINE + item.content + VERTICAL_LINE for item in column.items]
        # bottomLine = CONDUIT_SYMBOL + column.length * HORIZONTAL_LINE + CONDUIT_SYMBOL

        # matrixItem = stringListToMatrix([topLine] + middleLines + [bottomLine])

        matrixItem = ExtendableMatrix(defaultValue=SPACE, rows=[topLine] + middleLines + [bottomLine])

        currentX = self.builder.getCurrentX()
        currentY = self.builder.getCurrentY()

        conduitPoints = [
            (currentX, currentY), 
            (currentX, currentY + column.size + 1),
            (currentX + column.length + 1, currentY), 
            (currentX + column.length + 1, currentY + column.size + 1)
        ]

        return matrixItem, conduitPoints
    
    @returnList
    def _createColumnMiddleLines(self, column: Column):
        for item in column.items:
            yield self._createColumnMiddleLine(item)

    @returnList
    def _createColumnMiddleLine(self, item: ColumnItem):
        yield VERTICAL_LINE
        
        yield item.content[0] + getColor(item.color) + getStyle(item.style)

        for char in item.content[1:-1]:
            yield char

        yield item.content[-1] + RESET_STR_FORMAT_TAG

        yield VERTICAL_LINE


    def _cellConstructMethod(self, cell: Cell | EmptyCell):
        if isinstance(cell, Cell):
            matrixItem = self._constructNamedCell(cell)
        elif isinstance(cell, EmptyCell):
            matrixItem = self._constructEmptyCell(cell)

        currentX = self.builder.getCurrentX()
        currentY = self.builder.getCurrentY()

        conduitPoints = [
            (currentX, currentY),             
            (currentX, currentY + 2),
            (currentX + cell.length - 1, currentY), 
            (currentX + cell.length - 1, currentY + 2)
        ]
        
        return matrixItem, conduitPoints
    
    def _constructNamedCell(self, cell: Cell):
        horizontalPerimeterChar = HORIZONTAL_LINE
        verticalPerimeterChar = VERTICAL_LINE
        conduitChar = CONDUIT_SYMBOL

        line1 = conduitChar + horizontalPerimeterChar * len(cell.label) + conduitChar
        line2 = verticalPerimeterChar + cell.label + verticalPerimeterChar
        line3 = conduitChar + horizontalPerimeterChar * len(cell.label) + conduitChar

        return stringListToMatrix([line1, line2, line3])

    def _constructEmptyCell(self, cell: EmptyCell):
        return stringListToMatrix([SPACE * (cell.length + 2)] * 3)