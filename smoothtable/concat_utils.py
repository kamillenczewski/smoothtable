from .utils import ConvertTo, columnsToRows

@ConvertTo(list)
def RightConcat(stringListsArray: list[list[str]]):
    for row in columnsToRows(stringListsArray):
        yield ''.join(row)

@ConvertTo(list)
def LeftConcat(stringListsArray: list[list[str]]):
    for row in columnsToRows(stringListsArray[::-1]):
        yield ''.join(row)

@ConvertTo(list)
def TopConcat(stringListsArray: list[list[str]]):
    for list in stringListsArray[::-1]:
        for string in list:
            yield string

@ConvertTo(list)
def BottomConcat(stringListsArray: list[list[str]]):
    for list in stringListsArray:
        for string in list:
            yield string



@ConvertTo(list)
def rightConcat(*stringLists: list[str]):
    for row in columnsToRows(stringLists):
        yield ''.join(row)

@ConvertTo(list)
def leftConcat(*stringLists: list[str]):
    for row in columnsToRows(stringLists[::-1]):
        yield ''.join(row)

@ConvertTo(list)
def topConcat(*stringLists: list[str]):
    for list in stringLists[::-1]:
        for string in list:
            yield string

@ConvertTo(list)
def bottomConcat(*stringLists: list[str]):
    for list in stringLists:
        for string in list:
            yield string