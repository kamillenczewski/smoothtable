from typing import Iterable

from .cell import Cell
from .empty_cell import EmptyCell
from .utils import returnList, iterateNeighbors
from .constants import RANGE_LIMITS_SEPARATOR, SPACE, EMPTY


def removeSpace(string: str):
    return string.replace(SPACE, EMPTY)

@returnList
def stringLimitsToIntegers(limits: list[str]):
    for limit in limits:
        if limit.isdigit():
            yield int(limit)
        else:
            raise ValueError(f'Range should be composed of integer-like limits! Limits: {limits}')

@returnList
def stringRangesAndLabelsToCells(layer: dict[str, str]):
    for stringRange, label in layer.items():
        if not isinstance(stringRange, str):
            raise ValueError("'stringRange' should be string!")

        if not isinstance(label, str):
            raise ValueError("'label' should be string!")

        stringRange = removeSpace(stringRange)
        stringLimits = stringRange.split(RANGE_LIMITS_SEPARATOR)
        limits = stringLimitsToIntegers(stringLimits)
        limitsAmount = len(limits)

        if limitsAmount == 1:
            yield Cell((limits[0], limits[0] + 1), label)
        elif limitsAmount == 2:
            yield Cell((limits[0], limits[1]), label)
        else:
            raise ValueError(f'Range should consist of one or two limits! {limitsAmount}({limits}) were given!')

def sortCells(cells: list[Cell]):
    cells.sort(key=lambda cell: cell.cellsRange[0])

@returnList
def ensureRangesContinuity(cells: list[Cell]):
    for previousCell, currentCell in iterateNeighbors(cells, 2):
        yield previousCell

        if previousCell.cellsRange[1] < currentCell.cellsRange[0]:
            yield EmptyCell((previousCell.cellsRange[1], currentCell.cellsRange[0]))

        if previousCell.cellsRange[1] > currentCell.cellsRange[0]:
            raise ValueError('Two consecutive limits should be placed in ascending order!')

    yield cells[-1]

@returnList
def getIndexesLists(cells: list[list[Cell]]):
    for cellsList in cells:
        indexesList = list()

        for cell in cellsList:
            indexesList.extend(cell.lowerCellIndexes)

        yield indexesList

def validateRangeIndexes(cells: list[list[Cell]]):
    indexesLists = getIndexesLists(cells)

    for i in range(len(indexesLists)):
        lowerIndexesList = indexesLists[i]
        lowerCellsList = cells[i + 1]
        lowerCellsListLength = len(lowerCellsList)

        if not all(index < lowerCellsListLength for index in lowerIndexesList):
            raise ValueError(f'Layer with index: {i} has reference to lower indexes ({lowerIndexesList}) which are not included in lower layer!')

def normalizeAndValidateLayersGlobally(layers: Iterable[dict[str, str]]):
    if not isinstance(layers, Iterable):
        raise ValueError('Layers should be iterable!')
    
    validateRangeIndexes(layers)

def normalizeAndValidateSingleLayer(layer: dict[str, str]):
    if not isinstance(layer, dict):
        raise ValueError("Layer should be dictionary!")

    cells = stringRangesAndLabelsToCells(layer)
    sortCells(cells)
    cells = ensureRangesContinuity(cells)

    return cells

@returnList
def normalizeAndValidateLayers(layers: Iterable[dict[str, str]]):
    if isinstance(layers, dict):
        layers = [layers]
    
    if not isinstance(layers, Iterable):
        raise ValueError("Object 'layers' should be iterable object or dictionary!")

    for layer in layers:
        if not isinstance(layer, dict):
            raise ValueError("'lyaer' should be dictionary!")

        cells = stringRangesAndLabelsToCells(layer)
        sortCells(cells)
        cells = ensureRangesContinuity(cells)

        yield cells