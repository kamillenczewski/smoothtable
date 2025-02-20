from typing import Iterable

from .utils import (
    rowsToColumns, columnsToRows,
    stringifyColumns, leftConcat, 
    adjustColumns, adjustLabels, ConvertTo
)
from .painter import Painter
from .constants import *
from .column_labels import createColumnLabelsStringLines
from .row_labels import createRowLabelsStringLines
from .labels_normalization import normalize

@ConvertTo(list)
def getMaxStringLengths(columns):
    for column in columns:
        longestString = max(column, key=len)
        biggestLength = len(longestString)
        yield biggestLength





def createRowString(rowItems):
    return LEFT_VERTICAL_LINE + CENTER_VERTICAL_LINE.join(rowItems) + RIGHT_VERTICAL_LINE

def createRowsStringLines(columns):
    rows = columnsToRows(columns)
    rowsStrings = list(map(createRowString, rows))
    return rowsStrings




def createEndSegment(columnLengths, areRowLabels):
    separationLines = [length * HORIZONTAL_LINE for length in columnLengths]

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

@ConvertTo(list)
def adjustColumnLabelsAndRanges(labels, lengths):
    if isinstance(lengths, int):
        lengths = [lengths for _ in range(len(labels))]

    for (label, range), wantedLength in zip(labels, lengths):
        yield range, label.ljust(wantedLength, SPACE)
        


@ConvertTo(list)
def adjustStrings(strings, lengths):
    if isinstance(lengths, int):
        lengths = [lengths for _ in range(len(strings))]

    for string, wantedLength in zip(strings, lengths):
        yield string.ljust(wantedLength, SPACE)

@ConvertTo(list)
def adjustColumns(stringsArray, lengths):
    for column, length in zip(stringsArray, lengths):
        yield adjustLabels(column, length)

@ConvertTo(list)
def addSpaceAtStartAndAtEnd(columns):
    for column in columns:
        yield [SPACE + item + SPACE for item in column]

def addSpaceAtStartAndAtEndForLabels(labels):
    return [SPACE + item + SPACE for item in labels]

def adjustNeighboringLabelsLentghs(higherLayerLengths, higherLayerRanges, lowerLayerLengths):
    pass

def evaluateColumnLengthAndColumnLabelsLengths(columnLengths, columnLabelLengths, columnLabelRanges):
    newColumnLabelLengths = []
    newColumnLengths = columnLengths.copy()

    # columnLengthsGroups = [columnLengths[leftRangeLimit:rightRangeLimit + 1] for leftRangeLimit, rightRangeLimit in columnLabelRanges]

    for columnLabelLength, (leftRangeLimit, rightRangeLimit) in zip(columnLabelLengths, columnLabelRanges):
        columnsInRangeAmount = rightRangeLimit - leftRangeLimit + 1

        collectiveColumnsLength = sum(columnLengths[leftRangeLimit:rightRangeLimit + 1])
        separatorsLength = len(CENTER_VERTICAL_LINE) * (columnsInRangeAmount - 1)

        realColumnsLength = collectiveColumnsLength + separatorsLength


        newColumnLabelLength = columnLabelLength

        if realColumnsLength > columnLabelLength:
            newColumnLabelLength = realColumnsLength
        elif realColumnsLength < columnLabelLength:
            newColumnLengths[leftRangeLimit] += columnLabelLength - realColumnsLength

        newColumnLabelLengths.append(newColumnLabelLength)

    return newColumnLengths, newColumnLabelLengths

def createTable(columnLabels: Iterable[str] | dict[str, str], 
                rowLabels=None, 
                columns=None, 
                rows=None, 
                painter: Painter=None):

    # validation
    #validateArgs(columnLabels, rowLabels, columns, rows, painter)

    # normalization and intitialization
    # -------------- #
    if rows:
        columns = rowsToColumns(rows)

    areRowLabels = rowLabels != None
    areColumnLabels = columnLabels != None

    columnsAmount = len(columns)
    columnSize = len(columns[0])

    columnLabels = normalize(columnLabels, columnsAmount)
    columnLabelNames, columnLabelRanges = list(zip(*columnLabels))
    # -------------- #

    stringifiedColumns = stringifyColumns(columns)

    stringifiedColumns = addSpaceAtStartAndAtEnd(stringifiedColumns)
    columnLabelNames = addSpaceAtStartAndAtEndForLabels(columnLabelNames)
    
    columnLengths = getMaxStringLengths(stringifiedColumns)
    columnLabelLengths = list(map(len, columnLabelNames))

    columnLengths, columnLabelLengths = evaluateColumnLengthAndColumnLabelsLengths(columnLengths, columnLabelLengths, columnLabelRanges)
    
    columnLabelNames = adjustStrings(columnLabelNames, columnLabelLengths)
    stringifiedColumns = adjustColumns(stringifiedColumns, columnLengths)

    stringifiedColumns = adjustColumns(stringifiedColumns, columnLengths)

    if painter:
       colorMask = painter.createMask(columns, columnsAmount, columnSize)
       stringifiedColumns = painter.applyMask(stringifiedColumns, colorMask)

    columnLabelsStringLines = createColumnLabelsStringLines(columnLabelNames, columnLabelRanges, areRowLabels, columnLengths)
    rowsStringLines = createRowsStringLines(stringifiedColumns)
    endSegment = createEndSegment(columnLengths, areRowLabels)
    
    allLines = columnLabelsStringLines + rowsStringLines + [endSegment]

    if areRowLabels:
        rowLabelsStringLines = createRowLabelsStringLines(rowLabels)
        allLines = leftConcat(allLines, rowLabelsStringLines)
    
    return NEW_LINE.join(allLines)


"""
labels = [
    ('Name', (0, 3)), 
    ('__nolabel__', [4, 5]), 
    ('XDD', (6, 6)), 
    ('OLA', (7, 8)), 
    ('__nolabel__', [9, 10])
]
"""


"""
       ╭────┬────────────┬─────────────┬─────────────────╮
       │ Id │ First name │ Last name   │ Favourite Color │
╭──────┼────┼────────────┼─────────────┼─────────────────┤
│ Row1 │ 1  │ Kamil      │ Lenczewski  │ Blue            │
│ Row2 │ 2  │ Anastazja  │ Kasprzyk    │ Red             │
│ Row3 │ 3  │ Karolina   │ Olawska     │ Black           │
│ Row4 │ 4  │ Adam       │ Lewandowski │ Black           │
│ Row5 │ 5  │ Hania      │ Granat      │ Red             │
╰──────┴────┴────────────┴─────────────┴─────────────────╯
"""


"""

       ╭────┬────────────┬─────────────┬─────────────────╮
       │ Id │ First name │ Last name   │ Favourite Color │
╭──────┼────┼────────────┼─────────────┼─────────────────┤
"""