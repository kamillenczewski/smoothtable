from typing import Iterable

from .utils import (
    rowsToColumns, columnsToRows,
    stringifyColumns, leftConcat, 
    adjustColumns, adjustLabels
)

from .painter import Painter
from .constants import *

from .column_labels import createColumnLabelsStringLines
from .row_labels import createRowLabelsStringLines


def maxStringLengthGen(columns):
    for column in columns:
        longestString = max(column, key=len)
        biggestLength = len(longestString)
        yield biggestLength


def mergeLabelsAndColumnsGen(labels, columns):
    for label, column in zip(labels, columns):
        yield [label] + column



def createRowString(rowItems):
    return LEFT_VERTICAL_LINE + CENTER_VERTICAL_LINE.join(rowItems) + RIGHT_VERTICAL_LINE

def createRowsStringLines(columns):
    rows = columnsToRows(columns)
    rowsStrings = list(map(createRowString, rows))
    return rowsStrings




def createEndSegment(separationLines, areRowLabels):
    if areRowLabels:
        leftBottomCorner = BOTTOM_CENTER_CONDUIT
    else:
        leftBottomCorner = BOTTOM_LEFT_CORNER
    
    return leftBottomCorner + BOTTOM_CENTER_CONDUIT.join(separationLines) + BOTTOM_RIGHT_CORNER


def validateArgs(columnLabels, rowLabels, columns, rows, painter):
    if columns and rows:
        raise ValueError("Options 'columns' and 'rows' cannot be nonempty simultaneously! "
                         'Please choose only one of them!')

    if not columns and not rows:
        raise ValueError('Columns and rows cannot be empty simultaneously!'
                         'Please choose at least one of them!')


    if columns:
        if not all((length == len(columns[0]) for length in map(len, columns))):
            raise ValueError("All the columns should have the same size!")
        
        if rowLabels and not len(rowLabels) == len(columns[0]):
            raise ValueError("The number of row labels should be the same as rows size!")
        
        if columnLabels and not len(columnLabels) == len(columns):
            raise ValueError("The number of column labels should be the same as columns size!")

    if rows:
        if not all((length == len(rows[0]) for length in map(len, rows))):
            raise ValueError("All the rows should have the same size!")

        if rowLabels and not len(rowLabels) == len(rows):
            raise ValueError("The number of row labels should be the same as rows size!")
    
        if columnLabels and not len(columnLabels) == len(rows[0]):
            raise ValueError("The number of column labels should be the same as columns size!")


def createTable(columnLabels: Iterable[str], 
                rowLabels=None, 
                columns=None, 
                rows=None, 
                painter: Painter=None):

    #validateArgs(columnLabels, rowLabels, columns, rows, painter)

    if rows:
        columns = rowsToColumns(rows)

    columnsAmount = len(columns)
    columnSize = len(columns[0])

    colorMask = painter.createMask(columns, columnsAmount, columnSize)

    stringifiedColumns = stringifyColumns(columns)

    labelsAndColumns = list(mergeLabelsAndColumnsGen(columnLabels, stringifiedColumns))
    maxTextLentghs = list(maxStringLengthGen(labelsAndColumns))
    separationLines = [length * HORIZONTAL_LINE for length in maxTextLentghs]

    columnLabels = list(adjustLabels(columnLabels, maxTextLentghs))
    stringifiedColumns = list(adjustColumns(stringifiedColumns, maxTextLentghs))

    if painter:
       stringifiedColumns = painter.applyMask(stringifiedColumns, colorMask)

    areRowLabels = rowLabels != None
    areColumnLabels = columnLabels != None

    # maxTextLentghs ->? separationLines
    columnLabelsStringLines = createColumnLabelsStringLines(columnLabels, maxTextLentghs, areRowLabels)
    rowsStringLines = createRowsStringLines(stringifiedColumns)
    endSegment = createEndSegment(separationLines, areRowLabels)
    
    allLines = columnLabelsStringLines + rowsStringLines + [endSegment]

    if areRowLabels:
        rowLabelsStringLines = createRowLabelsStringLines(rowLabels)
        allLines = leftConcat(allLines, rowLabelsStringLines)
    
    return NEW_LINE.join(allLines)