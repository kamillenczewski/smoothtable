class EmptyCell:
    def __init__(self, cellsRange, length=None):
        if length:
            self.length = length + 2
        else:
            self.length = 2

        self.cellsRange = cellsRange
        self.lowerCellIndexes = list(range(*self.cellsRange))

    @property
    def label(self):
        return ' ' * self.length
    

    def copy(self):
        return EmptyCell(self.cellsRange, self.length)