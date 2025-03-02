class ExtendableMatrix:
    def __init__(self, defaultValue, width=None, height=None, rows=None):
        height, width = self._normalizeHeightAndWidth(width, height)
        self._validateHeightAndWidth(width, height)

        self.defaultValue = defaultValue

        if rows:
            self.rows = rows
        elif width and height:
            self.rows = [[self.defaultValue for _ in range(width)] for _ in range(height)]
        else:
            self.rows = [[defaultValue]]

    @staticmethod
    def _normalizeHeightAndWidth(height, width):
        if height and not width:
            width = 1

        if width and not height:
            height = 1

        return height, width

    @staticmethod
    def _validateHeightAndWidth(height, width):
        if not height and not width:
            return

        if not isinstance(height, int):
            raise ValueError("Variable 'height' has incorrect type! 'int' is needed!")

        if not isinstance(width, int):
            raise ValueError("Variable 'width' has incorrect type! 'int' is needed!")    

        if height <= 0:
            raise ValueError("'height' must be positive!")
        
        if width <= 0:
            raise ValueError("'width' must be positive!")

    def getHeight(self):
        return len(self.rows)

    def getWidth(self):
        return len(self.rows[0])


    def addDefaultRow(self):
        self.rows.append([self.defaultValue for _ in range(self.getWidth())])

    def addDefaultRows(self, number):
        for _ in range(number):
            self.addDefaultRow()

    def addDefaultColumns(self, number):
        for row in self.rows:
            row.extend([self.defaultValue] * number)


    def ensureHeightFor(self, y):
        if y < self.getHeight():
            return
    
        self.addDefaultRows(y + 1 - self.getHeight())
    
    def ensureWidthFor(self, x):
        if x < self.getWidth():
            return
    
        self.addDefaultColumns(x + 1 - self.getWidth())

    def putOther(self, x, y, other: 'ExtendableMatrix', highPriority=True):
        self.ensureWidthFor(x)
        self.ensureWidthFor(y)

        lowerExtremePointX = x + other.getWidth() - 1
        lowerExtremePointY = y + other.getHeight() - 1

        self.ensureWidthFor(lowerExtremePointX)
        self.ensureHeightFor(lowerExtremePointY)

        for currentX in range(x, lowerExtremePointX + 1):
            for currentY in range(y, lowerExtremePointY + 1):
                if highPriority or self.rows[currentY][currentX] == self.defaultValue:
                    self.rows[currentY][currentX] = other.rows[currentY - y][currentX - x]

    def getItem(self, x, y):
        if x < 0 or y < 0:
            return
        
        self.ensureWidthFor(x)
        self.ensureHeightFor(y)

        return self.rows[y][x]
    
    def setItem(self, x, y, item):
        if x < 0 or y < 0:
            return
        
        self.ensureWidthFor(x)
        self.ensureHeightFor(y)

        self.rows[y][x] = item

    def __str__(self):
        return '\n' + '\n'.join(''.join(map(str, row)) for row in self.rows) + '\n'