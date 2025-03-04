from typing import Iterable

from .utils import rowsToColumns, forEachInMatrix, returnList
from .painter import Painter
from .labels_normalization import validateLayersGlobally, normalizeAndValidateSingleLayer
from .constants import SPACE
from .cell import Cell
from .empty_cell import EmptyCell
from .color_condition import ColorCondition
from .column import Column
from .length_adjust_manager import LengthAdjustManager as _LengthAdjustManager
from .cells_builder import CellsBuilder


class SmoothtableBuilder:
    def __init__(self):
        self.columns: list[Column] = []
        self.painter = Painter()
        self.labelLayers: list[dict[str, str]] = []
    
    def _normalizeColumn(self, column):
        if isinstance(column, Iterable):
            return Column(column)
        elif isinstance(column, Column):
            return column
        else:
            raise ValueError('column has inproper!')        

    @returnList
    def _normalizeColumns(self, columns):
        for column in columns:
            yield self._normalizeColumn(column)
    
        

    def getColumnsAmount(self):
        return len(self.columns)
    
    def getColumnSize(self):
        return self.columns[0].length
    

    def setColumns(self, columns: list[list[str]]):
        if not all(len(column) == len(columns[0]) for column in columns):
            raise ValueError("All the columns should have the same size!")

        self.columns = self._normalizeColumns(columns)

        return self

    # TO DO
    def addColumn(self, column):
        column = self._normalizeColumn(column)

        if self.columns and self.columns[0].size != column.size:
            raise ValueError('Each added column should have the same size!')

        self.columns.append(column)

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

        # TO DO
        # Validating if the lowest labels number and columns amount are equal

        self._bothSidesIndentForColumns()
        self._bothSidesIndentForLabels()

        self._paintColumns()

        _LengthAdjustManager(self.labelLayers, self.columns).execute()

        matrixTable = CellsBuilder().appendRows(self.labelLayers).appendColumns(self.columns).build()
    
        return str(matrixTable)