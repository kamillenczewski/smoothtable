from .constants import CONDUIT_SYMBOL, CONDUITS


def returnList(generator):
    def iteratedGen(*args, **kwargs):
        return list(generator(*args, **kwargs))
    
    return iteratedGen



def iterateNeighbors(items, neighborNumber):
    for i in range(neighborNumber - 1, len(items)):
        yield tuple([items[i - k] for k in range(neighborNumber - 1, -1, -1)])



@returnList
def convertList(function, items):
    return list(map(function, items))

@returnList
def convertMatrix(function, matrix):
    for row in matrix:
        yield convertList(function, row)


def forEachInMatrix(function, matrix):
    for list in matrix:
        for item in list:
            function(item)


@returnList
def rowsToColumn(rows, columnIndex):
    for row in rows:
        yield row[columnIndex]

@returnList
def rowsToColumns(rows):
    for rowIndex in range(len(rows[0])):
        yield rowsToColumn(rows, rowIndex)


@returnList
def columnsToRow(columns, rowIndex):
    for column in columns:
        yield column[rowIndex]

@returnList
def columnsToRows(columns):
    for rowIndex in range(len(columns[0])):
        yield columnsToRow(columns, rowIndex)


def isConduit(char):
    if char == CONDUIT_SYMBOL:
        return True

    return char in CONDUITS