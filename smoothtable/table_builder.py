from .extendable_matrix import ExtendableMatrix
from .conduit_codes import CONDUIT_CODES_AND_CONDUITS
from .matrix_cell_builder import constructCell, constructEmptyCell, constructColumn
from .utils import returnList, isConduit
from .constants import SPACE


class NamedCell:
    def __init__(self, content):
        self.content = content
        self.length = len(content) + 2

class EmptyCell:
    def __init__(self, length):
        self.length = length + 2

class Column:
    def __init__(self, items, length):
        self.items = items
        self.length = length



class TableBuilder:
    def __init__(self):
        self.matrix = ExtendableMatrix(SPACE)

        self.conduitPoints = set()

        self.currentX = 0
        self.currentY = 0

    @staticmethod
    @returnList
    def _normalizeRow(row):
        for item in row:
            if isinstance(item, str):
                if item.isspace():
                    yield EmptyCell(len(item))
                else:
                    yield NamedCell(item)
            elif isinstance(item, int):
                yield EmptyCell(item)
            elif isinstance(item, NamedCell) or isinstance(item, EmptyCell):
                yield item
            else:
                raise ValueError(f'Item: {item} has inproper type!')

    @staticmethod
    @returnList
    def _normalizeColumns(columns):
        for column in columns:
            if isinstance(column, Column):
                yield column
            elif isinstance(column, tuple):
                yield Column(column[0], column[1])
            else:
                raise ValueError(f'Column: {column} has inproper type!')


    def setCurrentY(self, value):
        self.currentY = value
        return self

    def increaseCurrentY(self, value):
        self.currentY += value
        return self

    def setCurrentX(self, value):
        self.currentX = value
        return self

    def increaseCurrentX(self, value):
        self.currentX += value
        return self

    def addConduitPoints(self, *points):
        self.conduitPoints.update(points)

    def appendRow(self, row):
        row = self._normalizeRow(row)

        for cell in row:
            if isinstance(cell, NamedCell):
                cellMatrix = constructCell(cell.content)
                highPriority = True
            elif isinstance(cell, EmptyCell):
                cellMatrix = constructEmptyCell(cell.length)
                highPriority = False

            self.matrix.putOther(self.currentX, self.currentY, cellMatrix, highPriority)

            self.addConduitPoints((self.currentX, self.currentY), 
                                  (self.currentX, self.currentY + 2),
                                  (self.currentX + cell.length - 1, self.currentY), 
                                  (self.currentX + cell.length - 1, self.currentY + 2))

            self.increaseCurrentX(cell.length - 1)

        return self

    def appendRows(self, rows):
        startX = self.currentX

        for row in rows:
            self.appendRow(row)
            self.increaseCurrentY(2)
            self.setCurrentX(startX)
            print(self.matrix)

        return self
            

    def appendColumns(self, columns):
        columns = self._normalizeColumns(columns)

        for column in columns:
            names = column.items
            length = column.length
            namesAmount = len(names)

            columnMatrix = constructColumn(names, length)
            self.matrix.putOther(self.currentX, self.currentY, columnMatrix)


            self.addConduitPoints((self.currentX, self.currentY), 
                                  (self.currentX, self.currentY + namesAmount + 1),
                                  (self.currentX + length + 1, self.currentY), 
                                  (self.currentX + length + 1, self.currentY + namesAmount + 1))

            self.increaseCurrentX(length + 1)
        
        return self      

    def _createConduitCodes(self):
        for point in self.conduitPoints:
            x, y = point

            topCell = self.matrix.getItem(x, y - 1)
            bottomCell = self.matrix.getItem(x, y + 1)
            leftCell = self.matrix.getItem(x - 1, y)
            rightCell = self.matrix.getItem(x + 1, y)

            isTopConnected = isConduit(topCell)
            isBottomConnected = isConduit(bottomCell)
            isLeftConnected = isConduit(leftCell)
            isRightConnected = isConduit(rightCell)

            topCharCode = '1' if isTopConnected else '0'
            bottomCharCode = '1' if isBottomConnected else '0'
            leftCharCode = '1' if isLeftConnected else '0'
            rightCharCode = '1' if isRightConnected else '0'
            
            yield topCharCode + bottomCharCode + leftCharCode + rightCharCode


    def fixConduits(self):
        for point, code in zip(self.conduitPoints, self._createConduitCodes()):
            x, y = point
            conduitChar = CONDUIT_CODES_AND_CONDUITS[code]
            self.matrix.setItem(x, y, conduitChar)
            

    def build(self):
        self.fixConduits()
        return self.matrix