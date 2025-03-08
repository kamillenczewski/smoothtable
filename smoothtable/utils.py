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
def transposeMatrix(matrix):
    for arrayIndex in range(len(matrix[0])):
        yield [array[arrayIndex] for array in matrix]

def isConduit(char):
    if char == CONDUIT_SYMBOL:
        return True

    return char in CONDUITS

def writeFile(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def readFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()