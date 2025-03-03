from .extendable_matrix import ExtendableMatrix
from .constants import SPACE, HORIZONTAL_LINE, VERTICAL_LINE, CONDUIT_SYMBOL


def stringToChars(string):
    return [char for char in string]

def stringListToMatrix(strings):
    splitStrings = [stringToChars(string) for string in strings]
    return ExtendableMatrix(SPACE, rows=splitStrings)

def constructCell(content):
    horizontalPerimeterChar = HORIZONTAL_LINE
    verticalPerimeterChar = VERTICAL_LINE
    conduitChar = CONDUIT_SYMBOL

    line1 = conduitChar + horizontalPerimeterChar * len(content) + conduitChar
    line2 = verticalPerimeterChar + content + verticalPerimeterChar
    line3 = conduitChar + horizontalPerimeterChar * len(content) + conduitChar

    return stringListToMatrix([line1, line2, line3])

def constructEmptyCell(length):
    return stringListToMatrix([SPACE * (length + 2)] * 3)

def constructColumn(names, length): 
    """
    Consider instead of using pure string - ColumnItem whmatriich could hold color and type property
    and there attributes can be interpreted here to achive painting effect.
    """
    topLine = CONDUIT_SYMBOL + length * HORIZONTAL_LINE + CONDUIT_SYMBOL

    middleLines = [VERTICAL_LINE + name + VERTICAL_LINE for name in names]

    bottomLine = CONDUIT_SYMBOL + length * HORIZONTAL_LINE + CONDUIT_SYMBOL

    return stringListToMatrix([topLine] + middleLines + [bottomLine])

