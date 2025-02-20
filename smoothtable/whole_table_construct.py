from .constants import *
from .utils import returnList
from enum import Flag, auto

"""
╭──┬──────────┬─────────╮
│Id│First Name│Last Name│
├──┼──────────┼─────────┤
│Id│First Name│Last Name│
├──┼──────────┼─────────┤
│Id│First Name│Last Name│
├──┼──────────┴─────────╯
│Id│                   
├──┤          ╭─────────╮
│Id│          │Last Name│
├──┼──────────┼─────────┤
│Id│First Name│Last Name│
╰──┴──────────┴─────────╯

"""

class RowPosition(Flag):
    NULL = auto()
    START = auto()
    MIDDLE = auto()
    END = auto()

"""
╭────┬──┬────────╮
│Name│id│your mom│
├────┼──┼────────┤
│ Fa │ss│afsfssfs│
╰────┴──┴────────╯
"""


def constructTopLine(lengths: list[int]):
    return TOP_LEFT_CORNER + TOP_CENTER_CONDUIT.join(length * HORIZONTAL_LINE for length in lengths) + TOP_RIGHT_CORNER

def constructContentLine(names: list[str]):
    return LEFT_VERTICAL_LINE + CENTER_VERTICAL_LINE.join(names) + RIGHT_VERTICAL_LINE

def constructConduitLine(lengths: list[int]):
    return LEFT_CONDUIT + CENTER_CONDUIT.join(length * HORIZONTAL_LINE for length in lengths) + RIGHT_CONDUIT

def constructEndLine(lengths: list[int]):
    return BOTTOM_LEFT_CORNER + BOTTOM_CENTER_CONDUIT.join(length * HORIZONTAL_LINE for length in lengths) + BOTTOM_RIGHT_CORNER

@returnList
def insertBetween(items, betweenSeparator):
    for i in range(len(items) - 1):
        yield items[i]
        yield betweenSeparator
    
    yield items[-1]


def constructRow(row: list[str], rowPosition: RowPosition):
    # it depends on 'rowPosition' to implement...
    topLeftCorner = TOP_LEFT_CORNER
    topRightCorner = TOP_RIGHT_CORNER
    bottomLeftCorner = BOTTOM_LEFT_CORNER
    bottomRightCorner = BOTTOM_RIGHT_CORNER

    if RowPosition.START in rowPosition:
        bottomLeftCorner = LEFT_CONDUIT
        bottomRightCorner = RIGHT_CONDUIT

    if RowPosition.END in rowPosition:
        topLeftCorner = LEFT_CONDUIT
        topLeftCorner = RIGHT_CONDUIT

    if RowPosition.MIDDLE in rowPosition:
        topLeftCorner = LEFT_CONDUIT
        topRightCorner = RIGHT_CONDUIT
        bottomLeftCorner = LEFT_CONDUIT
        bottomRightCorner = RIGHT_CONDUIT

    horizontalLines = [len(name) * HORIZONTAL_LINE for name in row]

    topLine = topLeftCorner + TOP_CENTER_CONDUIT.join(horizontalLines) + topRightCorner
    middleLine = CENTER_VERTICAL_LINE + CENTER_VERTICAL_LINE.join(row) + CENTER_VERTICAL_LINE
    bottomLine = bottomLeftCorner + BOTTOM_CENTER_CONDUIT.join(horizontalLines) + bottomRightCorner

    return [topLine, middleLine, bottomLine]

@returnList
def constructTable2(rows: list[list[str]]):
    lengths = list(map(len, rows[0]))

    yield constructTopLine(lengths)

    conduitLine = constructConduitLine(lengths)
    contentLines = [constructContentLine(row) for row in rows]

    innerLines = insertBetween(contentLines, conduitLine)
    
    for line in innerLines:
        yield line

    yield constructEndLine(lengths)


@returnList
def constructTable(rows: list[list[str]]):
    for index, row in enumerate(rows):
        rowPosition = RowPosition.NULL

        firstIndex = 0
        lastIndex = len(rows) - 1

        if index == firstIndex:
            rowPosition |= RowPosition.START
        
        if index == lastIndex:
            rowPosition |= RowPosition.END

        if firstIndex < index < lastIndex:
            rowPosition |= RowPosition.MIDDLE

        for string in constructRow(row, rowPosition):
            yield string

def main():
    rows = [
        ['Id', 'First Name', 'Last Name'],
        ['Id', 'First Name', 'Last Name'],
        ['Id', 'First Name', 'Last Name'],
        ['Id', 'First Name', 'Last Name'],
        ['Id', 'First Name', 'Last Name'],
        ['Id', 'First Name', 'Last Name']
    ]
    result = constructTable2(rows)
    result = NEW_LINE.join(result)
    print(result)