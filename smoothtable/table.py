from typing import Iterable

from .utils import rowsToColumns, returnList, convertMatrix, forEachInMatrix
from .painter import Painter
from .labels_normalization import normalizeAndValidateLayers, normalizeAndValidateLayersGlobally, normalizeAndValidateSingleLayer
from .table_builder import TableBuilder
from .length_adjust_manager import LengthAdjustManager
from .constants import SPACE
from .cell import Cell
from .color_condition import ColorCondition


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
    
    validateColumnsAndRows(columns, rows)
    columnLabels = normalizeAndValidateLayers(columnLabels)

    if rows:
        columns = rowsToColumns(rows)

    columns = stringifyColumns(columns) 
    # createColumns (METHOD) each list-like column is converted to Column Object

    if painter:
       columns = painter.paint(columns)

    columns = bothSidesIndentForColumns(columns)

    bothSidesIndentForLabels(columnLabels)

    LengthAdjustManager(columnLabels, columns).execute()


    labelsLayers = convertMatrix(lambda cell: cell.label, columnLabels)

    table = TableBuilder().appendRows(labelsLayers).appendColumns(columns).build()
    
    return str(table)


class SmoothtableBuilder:
    def __init__(self):
        self.columns: list[list[Cell]] = None
        self.painter = Painter()
        self.labelLayers: list[dict[str, str]] = None
    
    
    def getColumnsAmount(self):
        return len(self.columns)
    
    def getColumnSize(self):
        return len(self.columns[0])
    

    def setColumns(self, columns: list[list[str]]):
        if not all(len(column) == len(columns[0]) for column in columns):
            raise ValueError("All the columns should have the same size!")

        self.columns = columns
        return self

    def setRows(self, rows: list[list[str]]):
        if not all(len(row) == len(rows[0]) for row in rows):
            raise ValueError("All the rows should have the same size!")

        self.columns = rowsToColumns(rows)
        return self
    
    def addColorCondition(self, colorCondition: ColorCondition):
        self.painter.addColorCondition(colorCondition)
        return self
    
    def putLabelLayer(self, layer: dict[str, str]):
        layer = normalizeAndValidateSingleLayer(layer)
        self.labelLayers.append(layer)
        return self
    
    def build(self):
        normalizeAndValidateLayersGlobally(self.labelLayers)

        table = TableBuilder().appendRows(self.labelLayers).appendColumns(self.columns).build()
    
        return str(table)