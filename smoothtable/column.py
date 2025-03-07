from .constants import SPACE
from .column_item import ColumnItem
from .utils import returnList


class Column:
    def __init__(self, items: list[ColumnItem]):
        self.items = self._normalizeItems(items)
        self._length = max(map(len, self.items))

        self.adjustRight(self._length)
    
    @returnList
    def _normalizeItems(self, items):
        for item in items:
            if isinstance(item, str):
                yield ColumnItem(item)
            elif isinstance(item, ColumnItem):
                yield item
            else:
                raise ValueError('Inproper type of item! ColumnItem or str expected!')
    
    @property
    def size(self):
        return len(self.items)
    
    @property
    def length(self):
        return self._length

    def leftInsert(self, string):
        self._length += len(string)

        for item in self.items:
            item.content = string + item.content

    def rightInsert(self, string):
        self._length += len(string)

        for item in self.items:
            item.content = item.content + string

    def adjustRight(self, length, fillChar=SPACE):
        if length <= self._length:
            return

        if not isinstance(fillChar, str):
            raise ValueError('fillChar must be a string!')
        
        if len(fillChar) != 1:
            raise ValueError('fillChar must be made up of one character!')

        self._length = length

        for item in self.items:
            item.content = item.content.ljust(length, fillChar)


    def adjustLeft(self, length, fillChar=SPACE):
        if length <= self._length:
            return

        if not isinstance(fillChar, str):
            raise ValueError('fillChar must be a string!')
        
        if len(fillChar) != 1:
            raise ValueError('fillChar must be made up of one character!')
        
        self._length = length

        for item in self.items:
            item.content = item.content.rjust(length, fillChar)

    def __setitem__(self, index, value):
        self.items[index] = value

    def __getitem__(self, index):
        return self.items[index]
    
    def __len__(self):
        return self.size