from typing import Iterable

from .utils import rowsToColumns, returnList, convertMatrix, forEachInMatrix
from .painter import Painter
from .labels_normalization import normalizeAndValidateLayers, validateLayersGlobally, normalizeAndValidateSingleLayer
from .table_builder import TableBuilder
from .length_adjust_manager import LengthAdjustManager
from .constants import SPACE
from .cell import Cell
from .empty_cell import EmptyCell
from .color_condition import ColorCondition
from .column import Column

from .___length_adjust_manager import LengthAdjustManager as _LengthAdjustManager
from .___cells_builder import CellsBuilder

def validateColumnsAndRows(columns, rows):
    if columns and rows:
        raise ValueError("Options 'columns' and 'rows' cannot be nonempty simultaneously! "
                         'Please choose only one of them!')

    if not columns and not rows:
        raise ValueError('Columns and rows cannot be empty simultaneously!'
                         'Please choose at least one of them!')

    if columns:
        if not all(len(column) == len(columns[0]) for column in columns):
            raise ValueError("All the columns should have the same size!")

    if rows:
        if not all(len(row) == len(rows[0]) for row in rows):
            raise ValueError("All the rows should have the same size!")

        


@returnList
def stringifyColumns(columns):
    for column in columns:
        yield list(map(str, column))

@returnList
def normalizeColumns(columns: list[list[str]]):
    for column in columns:
        maxColumnLength = max(map(len, column))

        yield Column(column, maxColumnLength)



def bothSidesIndentForColumns(columns):
    return convertMatrix(lambda item: SPACE + item + SPACE, columns)



def bothSidesIndentForLabels(cells):
    def indentLabel(cell):
        if isinstance(cell, Cell):
            cell.label = SPACE + cell.label + SPACE

    forEachInMatrix(indentLabel, cells)


def createTable(columnLabels: Iterable[str] | dict[str, str], 
                columns=None, 
                rows=None, 
                painter: Painter=None):
    
    validateColumnsAndRows(columns, rows) # + 
    columnLabels = normalizeAndValidateLayers(columnLabels) # + 

    if rows: # + 
        columns = rowsToColumns(rows) # + 

    columns = stringifyColumns(columns)  # + 

    if painter: # + 
       columns = painter.paint(columns) # + 

    columns = bothSidesIndentForColumns(columns) # + 

    bothSidesIndentForLabels(columnLabels) # + 

    LengthAdjustManager(columnLabels, columns).execute()


    labelsLayers = convertMatrix(lambda cell: cell.label, columnLabels)

    table = TableBuilder().appendRows(labelsLayers).appendColumns(columns).build()
    
    return str(table)


class SmoothtableBuilder:
    def __init__(self):
        self.columns: list[Column] = None
        self.painter = Painter()
        self.labelLayers: list[dict[str, str]] = []
    
    
    def getColumnsAmount(self):
        return len(self.columns)
    
    def getColumnSize(self):
        return self.columns[0].length
    

    def setColumns(self, columns: list[list[str]]):
        if not all(len(column) == len(columns[0]) for column in columns):
            raise ValueError("All the columns should have the same size!")

        self.columns = normalizeColumns(columns)

        return self

    def setRows(self, rows: list[list[str]]):
        if not all(len(row) == len(rows[0]) for row in rows):
            raise ValueError("All the rows should have the same size!")

        return self.setColumns(rowsToColumns(rows))
    
    def addColorCondition(self, colorCondition: ColorCondition):
        self.painter.addColorCondition(colorCondition)
        return self
    
    def putLabelLayer(self, layer: dict[str, str]):
        layer = normalizeAndValidateSingleLayer(layer)
        self.labelLayers.append(layer)
        return self
    
    def _paintColumns(self):
        if self.painter and False:
            self.columns = self.painter.paint(self.columns, self.getColumnsAmount(), self.getColumnSize())

    def _bothSidesIndentForColumns(self):
        for column in self.columns:
            column.rightInsert(SPACE)
            column.leftInsert(SPACE)

    
    def _bothSidesIndentForLabels(self):
        def indentLabel(cell: Cell | EmptyCell):
            if isinstance(cell, Cell):
                cell.label = SPACE + cell.label + SPACE

        forEachInMatrix(indentLabel, self.labelLayers)

    def build(self):
        #validateLayersGlobally(self.labelLayers)

        self._bothSidesIndentForColumns()
        self._bothSidesIndentForLabels()

        self._paintColumns()

        _LengthAdjustManager(self.labelLayers, self.columns).execute()

        matrixTable = CellsBuilder().appendRows(self.labelLayers).appendColumns(self.columns).build()
    
        return str(matrixTable)