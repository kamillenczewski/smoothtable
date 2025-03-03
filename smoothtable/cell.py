class Cell:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            self.cellsRange = args[0][0]
            self._label = args[0][1]
        elif len(args) == 2 and isinstance(args[0], tuple) and isinstance(args[1], str):
            self.cellsRange = args[0]
            self._label = args[1]
        else:
            raise ValueError('Invalid number of arguments passed!')
            
        self.lowerCellIndexes = list(range(*self.cellsRange))

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return len(self.label) + 2
    
    @label.setter
    def label(self, value):
        self._label = value

    # TO CHANGE TO RIGHT AND LEFT ADJUST...
    @length.setter
    def length(self, value):
        self.label = self.label.ljust(value)
