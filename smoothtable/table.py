from typing import Iterable

from .utils import (
    rowsToColumns, stringifyColumns, leftConcat, 
    adjustColumns, adjustLabels, adjustLabelsGen
)

from .painter import Painter

HORIZONTAL_LINE = '─'

LEFT_VERTICAL_LINE = '│ '
RIGHT_VERTICAL_LINE = ' │'
CENTER_VERTICAL_LINE = ' │ '

TOP_LEFT_CORNER = '╭─'
TOP_RIGHT_CORNER = '─╮'

BOTTOM_LEFT_CORNER = '╰─'
BOTTOM_RIGHT_CORNER = '─╯'

CENTER_CONDUIT = '─┼─'
TOP_CENTER_CONDUIT = '─┬─'
BOTTOM_CENTER_CONDUIT = '─┴─'
LEFT_CONDUIT = '├─'
RIGHT_CONDUIT = '─┤'

NEW_LINE = '\n'
SPACE = ' '

def createColumnLabelsStringLines(labels, separationLines, areRowLabels):
    if areRowLabels:
        leftBottomCorner = CENTER_CONDUIT
    else:
        leftBottomCorner = LEFT_CONDUIT

    segment1 = TOP_LEFT_CORNER + TOP_CENTER_CONDUIT.join(separationLines) + TOP_RIGHT_CORNER
    segment2 = LEFT_VERTICAL_LINE + CENTER_VERTICAL_LINE.join(labels) + RIGHT_VERTICAL_LINE
    segment3 = leftBottomCorner + CENTER_CONDUIT.join(separationLines) + RIGHT_CONDUIT

    return [segment1, segment2, segment3]


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




def columnsToRow(columns, rowIndex):
    for column in columns:
        yield column[rowIndex]

def columnsToRows(columns):
    for rowIndex in range(len(columns[0])):
        yield list(columnsToRow(columns, rowIndex))




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
        
        if not len(rowLabels) == len(columns[0]):
            raise ValueError("The number of row labels should be the same as rows size!")
        
        if not len(columnLabels) == len(columns):
            raise ValueError("The number of column labels should be the same as columns size!")

    if rows:
        if not all((length == len(rows[0]) for length in map(len, rows))):
            raise ValueError("All the rows should have the same size!")

        if not len(rowLabels) == len(rows):
            raise ValueError("The number of row labels should be the same as rows size!")
    
        if not len(columnLabels) == len(rows[0]):
            raise ValueError("The number of column labels should be the same as columns size!")


def createTable(columnLabels: Iterable[str], 
                rowLabels=None, 
                columns=None, 
                rows=None, 
                painter: Painter=None):

    validateArgs(columnLabels, rowLabels, columns, rows, painter)

    if rows:
        columns = rowsToColumns(rows)

    columnsAmount = len(columns)
    columnSize = len(columns[0])

    colorMesh = painter.createMesh(columns, columnsAmount, columnSize)

    stringifiedColumns = stringifyColumns(columns)

    labelsAndColumns = mergeLabelsAndColumnsGen(columnLabels, stringifiedColumns)
    maxTextLentghs = list(maxStringLengthGen(labelsAndColumns))
    separationLines = [length * HORIZONTAL_LINE for length in maxTextLentghs]

    columnLabels = list(adjustLabels(columnLabels, maxTextLentghs))
    stringifiedColumns = list(adjustColumns(stringifiedColumns, maxTextLentghs))

    if painter:
       stringifiedColumns = painter.applyMesh(stringifiedColumns, colorMesh)

    areRowLabels = rowLabels != None
    areColumnLabels = columnLabels != None

    columnLabelsStringLines = createColumnLabelsStringLines(columnLabels, separationLines, areRowLabels)
    rowsStringLines = createRowsStringLines(stringifiedColumns)
    endSegment = createEndSegment(separationLines, areRowLabels)
    
    allLines = columnLabelsStringLines + rowsStringLines + [endSegment]

    if areRowLabels:
        rowLabelsStringLines = createRowLabelsStringLines(rowLabels)
        allLines = leftConcat(allLines, rowLabelsStringLines)
    
    return NEW_LINE.join(allLines)


def createRowLabelsStringLines(rowLabels):
    def createRowLabelLines(labels):
        for label in labels:
            yield LEFT_VERTICAL_LINE + label + SPACE

    maxLength = len(max(rowLabels, key=len))
    labels = adjustLabelsGen(rowLabels, maxLength)

    spaceLines = [(maxLength + 3) * SPACE] * 2

    beginningLine = TOP_LEFT_CORNER + HORIZONTAL_LINE * maxLength
    middleLines = list(createRowLabelLines(labels))
    endLine = BOTTOM_LEFT_CORNER + HORIZONTAL_LINE * maxLength

    allLines = spaceLines + [beginningLine] + middleLines + [endLine]

    return allLines

def main():
    table = createTable(
        columnLabels=['Id', 'First name', 'Last name', 'Favourite Color'],
        rowLabels=['Row1', 'Row2', 'Row3'],
        rows=[
            ["1", 'Kamil', 'Lenczewski', 'Blue'],
            ["2", 'Anastazja', 'Kasprzyk', 'Red'],
            ["3", 'Karolina', 'Olawska', 'Black'],
        ]
    )

    print(table)

if __name__ == '__main__':
    main()