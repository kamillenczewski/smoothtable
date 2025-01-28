from .constants import SPACE

def returnList(generator):
    def iteratedGen(*args, **kwargs):
        return list(generator(*args, **kwargs))
    
    return iteratedGen

# Columns to rows conversion

@returnList
def columnsToRow(columns, rowIndex):
    for column in columns:
        yield column[rowIndex]

def columnsToRowsGen(columns):
    for rowIndex in range(len(columns[0])):
        yield columnsToRow(columns, rowIndex)

def columnsToRows(columns):
    return list(columnsToRowsGen(columns))



# Rows to columns conversion

def rowsToColumnGen(rows, columnIndex):
    for row in rows:
        yield row[columnIndex]

def rowsToColumn(rows, columnIndex):
    return list(rowsToColumnGen(rows, columnIndex))

def rowsToColumnsGen(rows):
    for rowIndex in range(len(rows[0])):
        yield rowsToColumn(rows, rowIndex)

def rowsToColumns(rows):
    return list(rowsToColumnsGen(rows))



# Other utils

def stringifyColumnsGen(columns):
    for column in columns:
        yield list(map(str, column))

def stringifyColumns(columns):
    return list(stringifyColumnsGen(columns))

def leftConcatGen(lines, linesToAdd):
    for lineToAdd, line in zip(linesToAdd, lines):
        yield lineToAdd + line

def leftConcat(lines, linesToAdd):
    return list(leftConcatGen(lines, linesToAdd))



# adjusting

def adjustLabelsGen(labels, lengths):
    if isinstance(lengths, int):
        lengths = [lengths for _ in range(len(labels))]

    for label, wantedLength in zip(labels, lengths):
        yield label.ljust(wantedLength, SPACE)

def adjustLabels(labels, lengths):
    return list(adjustLabelsGen(labels, lengths))

@returnList
def adjustColumnGen(column, stringLength):
    for item in column:
        yield item.ljust(stringLength, SPACE)

@returnList
def adjustColumns(columns, maxTextLentghs):
    for column, maxLength in zip(columns, maxTextLentghs):
        yield adjustColumnGen(column, maxLength)