from .constants import *
from .utils import adjustLabels

def createRowLabelLines(labels):
    for label in labels:
        yield LEFT_VERTICAL_LINE + label

def createRowLabelsStringLines(rowLabels):
    maxLength = len(max(rowLabels, key=len))
    labels = adjustLabels(rowLabels, maxLength)

    spaceLines = [(maxLength + 1) * SPACE] * 2

    beginningLine = TOP_LEFT_CORNER + HORIZONTAL_LINE * maxLength
    middleLines = list(createRowLabelLines(labels))
    endLine = BOTTOM_LEFT_CORNER + HORIZONTAL_LINE * maxLength

    allLines = spaceLines + [beginningLine] + middleLines + [endLine]

    return allLines