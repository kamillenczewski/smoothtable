from .constants import SPACE

def returnList(generator):
    def iteratedGen(*args, **kwargs):
        return list(generator(*args, **kwargs))
    
    return iteratedGen

# consider using convertTo istead of ConvertTO
class ConvertTo:
    def __init__(self, *convertMethods):
        self.convertMethods = convertMethods

    def __call__(self, funcToConvert):
        def converted(*args, **kwargs):
            func = funcToConvert(*args, **kwargs)

            for method in self.convertMethods:
                func = method(func)

            return func
        
        return converted

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

@returnList
def leftConcat(lines, linesToAdd):
    for lineToAdd, line in zip(linesToAdd, lines):
        yield lineToAdd + line

@returnList
def rightConcat(lines, linesToAdd):
    for lineToAdd, line in zip(linesToAdd, lines):
        yield line + lineToAdd

@returnList
def rightConcat__(stringListsArray: list[list[str]]):
    for row in columnsToRows(stringListsArray):
        yield ''.join(row)

# adjusting

def adjustLabelsGen(labels, lengths):
    if isinstance(lengths, int):
        lengths = [lengths for _ in range(len(labels))]

    for label, wantedLength in zip(labels, lengths):
        yield label.ljust(wantedLength, SPACE)

def adjustLabels(labels, lengths):
    return list(adjustLabelsGen(labels, lengths))


@ConvertTo(list)
def adjustColumnLabelsAndRanges(labels, lengths):
    if isinstance(lengths, int):
        lengths = [lengths for _ in range(len(labels))]

    for (label, range), wantedLength in zip(labels, lengths):
        yield range, label.ljust(wantedLength, SPACE)


@returnList
def adjustColumnGen(column, stringLength):
    for item in column:
        yield item.ljust(stringLength, SPACE)

@returnList
def adjustColumns(columns, maxTextLentghs):
    for column, maxLength in zip(columns, maxTextLentghs):
        yield adjustColumnGen(column, maxLength)