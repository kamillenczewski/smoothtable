class ColumnItem:
    def __init__(self, content):
        self.content = content
        self.color = None
        self.style = None

    def __len__(self):
        return len(self.content)