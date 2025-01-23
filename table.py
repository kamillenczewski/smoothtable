from typing import Iterable

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

def adjustLabels(labels, lengths):
    if isinstance(lengths, int):
        lengths = [lengths for _ in range(len(labels))]

    for label, wantedLength in zip(labels, lengths):
        yield label.ljust(wantedLength, SPACE)

def adjustColumn(column, stringLength):
    for item in column:
        yield item.ljust(stringLength, SPACE)

def adjustColumns(columns, maxTextLentghs):
    for column, maxLength in zip(columns, maxTextLentghs):
        yield list(adjustColumn(column, maxLength))

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

def stringifyColumns(columns):
    for column in columns:
        yield list(map(str, column))

def rowsToColumn(rows, columnIndex):
    for row in rows:
        yield row[columnIndex]

def rowsToColumns(rows):
    for rowIndex in range(len(rows[0])):
        yield rowsToColumn(rows, rowIndex)

def leftConcat(lines, linesToAdd):
    for lineToAdd, line in zip(linesToAdd, lines):
        yield lineToAdd + line

def createEndSegment(separationLines, areRowLabels):
    if areRowLabels:
        leftBottomCorner = BOTTOM_CENTER_CONDUIT
    else:
        leftBottomCorner = BOTTOM_LEFT_CORNER
    
    return leftBottomCorner + BOTTOM_CENTER_CONDUIT.join(separationLines) + BOTTOM_RIGHT_CORNER

def createTable(columnLabels: Iterable[str], rowLabels=None, columns=None, rows=None, painter=None):
    if rows:
        columns = list(rowsToColumns(rows))

    columns = list(stringifyColumns(columns))

    labelsAndColumns = mergeLabelsAndColumnsGen(columnLabels, columns)
    maxTextLentghs = list(maxStringLengthGen(labelsAndColumns))
    separationLines = [length * HORIZONTAL_LINE for length in maxTextLentghs]

    columnLabels = list(adjustLabels(columnLabels, maxTextLentghs))
    columns = list(adjustColumns(columns, maxTextLentghs))

    if painter:
       columns = painter.paint(columns)

    areRowLabels = rowLabels != None

    columnLabelsStringLines = createColumnLabelsStringLines(columnLabels, separationLines, areRowLabels)
    rowsStringLines = createRowsStringLines(columns)
    endSegment = createEndSegment(separationLines, areRowLabels)
    
    allLines = columnLabelsStringLines + rowsStringLines + [endSegment]

    if areRowLabels:
        rowLabelsStringLines = createRowLabelsStringLines(rowLabels)
        allLines = list(leftConcat(allLines, rowLabelsStringLines))
    
    return NEW_LINE.join(allLines)


def createRowLabelsStringLines(rowLabels):
    def createRowLabelLines(labels):
        for label in labels:
            yield LEFT_VERTICAL_LINE + label + SPACE

    maxLength = len(max(rowLabels, key=len))
    labels = adjustLabels(rowLabels, maxLength)

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