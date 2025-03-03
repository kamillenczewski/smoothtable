from .constants import SPACE

class Column:
    def __init__(self, items):
        self.items = items
        self.length = max(map(len, self.items))

        self.adjustRight(self.length)
        
    @property
    def size(self):
        return len(self.items)
    
    def leftInsert(self, string):
        self.length += len(string)
        self.items = [string + item for item in self.items]

    def rightInsert(self, string):
        self.length += len(string)
        self.items = [item + string for item in self.items]

    def adjustRight(self, length, fillChar=SPACE):
        if length <= len(self.items):
            return

        if not isinstance(fillChar, str):
            raise ValueError('fillChar must be a string!')
        
        if len(fillChar) != 1:
            raise ValueError('fillChar must be made up of one character!')

        self.length = length

        self.items = [item.ljust(length, fillChar) for item in self.items]

    def adjustLeft(self, length, fillChar=SPACE):
        if length <= len(self.items):
            return

        if not isinstance(fillChar, str):
            raise ValueError('fillChar must be a string!')
        
        if len(fillChar) != 1:
            raise ValueError('fillChar must be made up of one character!')
        
        self.length = length
        self.items = [item.rjust(length, fillChar) for item in self.items]