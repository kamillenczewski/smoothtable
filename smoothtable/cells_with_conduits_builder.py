from .extendable_matrix import ExtendableMatrix

SPACE = ' '

class CellsWithConduitsBuilder:
    def __init__(self, isConduitMethod, conduitCodesAndConduits):
        self.isConduitMethod = isConduitMethod
        self.conduitCodesAndConduits = conduitCodesAndConduits

        self.matrix = ExtendableMatrix(SPACE)

        self.conduitPoints = list()#set()

        self.currentX = 0
        self.currentY = 0

        self.constructMethod = None

        self.isHighPriority = True

    def getCurrentX(self):
        return self.currentX
    
    def getCurrentY(self):
        return self.currentY


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




    def withConstructMethod(self, constructMethod):
        self.constructMethod = constructMethod
        return self
    
    def withItemHighPriority(self):
        self.isHighPriority = True
        return self

    def withItemLowPriority(self):
        self.isHighPriority = False
        return self
        
    def append(self, item):
        if not self.constructMethod:
            raise ValueError('To append item you need to apply constructing method!')

        matrixItem, conduitPoints = self.constructMethod(item)

        self.matrix.putOther(self.currentX, self.currentY, matrixItem, self.isHighPriority)

        self._addConduitPoints(conduitPoints)

        return self

    def build(self):
        print(str(self.matrix))
        self._fixConduits()
        return self.matrix


    def _addConduitPoints(self, points):
        self.conduitPoints.extend(points)   

    def _createConduitCodes(self):
        for point in self.conduitPoints:
            x, y = point

            topCell = self.matrix.getItem(x, y - 1)
            bottomCell = self.matrix.getItem(x, y + 1)
            leftCell = self.matrix.getItem(x - 1, y)
            rightCell = self.matrix.getItem(x + 1, y)

            isTopConnected = self.isConduitMethod(topCell)
            isBottomConnected = self.isConduitMethod(bottomCell)
            isLeftConnected = self.isConduitMethod(leftCell)
            isRightConnected = self.isConduitMethod(rightCell)

            topCharCode = '1' if isTopConnected else '0'
            bottomCharCode = '1' if isBottomConnected else '0'
            leftCharCode = '1' if isLeftConnected else '0'
            rightCharCode = '1' if isRightConnected else '0'
            
            yield topCharCode + bottomCharCode + leftCharCode + rightCharCode


    def _fixConduits(self):
        codes = list(self._createConduitCodes())

        for point, code in zip(self.conduitPoints, codes):
            x, y = point
            conduitChar = self.conduitCodesAndConduits[code]
            self.matrix.setItem(x, y, conduitChar)
            