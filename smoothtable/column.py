class Column:
    def __init__(self, items, length):
        self.items = items
        self.length = length
        
    @property
    def size(self):
        return len(self.items)