from .constants import *
from .utils import returnList
from .concat_utils import *

"""
Instead of creating line constructing methods
we can consider using cell construction
and then concatenate them along.
"""

"""
top left cell
C──────────C
│First Name│
C──────────C
"""

"""
top middle cell
─────────C
Last Name│
─────────C
"""

"""
3 top cells (top, middle, middle)
C──────────C ─────────C ────────C
│First Name│ Last Name│  COS    │
C──────────C ─────────C ────────C
"""

"""
EMPTY LABEL EXAMPLE
C──────────C           C────────C
│First Name│  [EMPTY]  │  COS   │
C──────────C           C────────C
"""

"""
bottom left cell
│Id│
C──C
"""

"""
bottom middle cell
 First    │
──────────C
"""

"""
4 bottom cells (left, middle, middle, middle):
│Id│ First    │Last Name│ COS    │
C──C──────────C─────────C────────C
"""

"""
top left empty label -> checks if next is empty
    if yes then it has horizontal lines on corners and space between them
    if no then it has conduit symbols on corners and vertical line between them
"""


"""
   C──────────C─────────C────────C
   │First Name│Last Name│ COS    │
C──C──────────C─────────C────────C
│Id│ First    │Last Name│ COS    │
C──C──────────C─────────C────────C

              C─────────C
              │Last Name│
C──C──────────C─────────C
│Id│ First    │Last Name│
C──C──────────C─────────C


C──C          C─────────C
│Id│          │Last Name│
C──C──────────C─────────C
│Id│ First    │Last Name│
C──C──────────C─────────C

C──C                    C────────C
│Id│                    │ COS    │
C──C──────────C─────────C────────C
│Id│ First    │Last Name│ COS    │
C──C──────────C─────────C────────C
"""

def listToString(items):
    return EMPTY.join(items)

@returnList
def listJoin(separator, items):
    if not items:
        return []

    for i in range(len(items) - 1):
        yield items[i]
        yield separator
    
    yield items[-1]

class Label:
    def __init__(self, range, name):
        self.range = range
        self.name = name


class Layer:
    def __init__(self, labels):
        self.labels = labels

    def getNames(self):
        return [label.name for label in self.labels]

    def getLengths(self):
        return list(map(len, self.getNames()))

CONDUIT_SYMBOL = '__conduit__'
CONDUIT_SYMBOL = 'C'
layers = [
    [Label((0,0), 'First Name'), Label((1,1), 'Second Name'), Label((2,2), 'Id'), Label((3,3), 'Favourite Color')]
]

def createLayer(ranges, names):
    return Layer([Label(range, name) for range, name in zip(ranges, names)])

def constructHorizontalLine(lengths: list[int]):
    return (sum(lengths) + len(lengths) + 1) * HORIZONTAL_LINE

class ContentLineBuilder:
    def __init__(self, names, lengths):
        self.names = names
        self.lengths = lengths
        self.size = len(self.names)
        self.currentIndex = -1

    def tryNextIndex(self):
        if self.currentIndex + 1 >= self.size:
            return False

        self.currentIndex += 1

        return True

    def getCurrentName(self):
        return self.names[self.currentIndex]

    @returnList
    def construct(self):
        spaceIndexes = []

        while True:
            if not self.tryNextIndex():
                break

            name = self.getCurrentName()

  

            if name.isspace():
                spaceIndexes.append(self.currentIndex)
            else:
                if spaceIndexes:
                    for index in spaceIndexes[-1]:
                        yield self.lengths[index] * (SPACE + 1)

                    yield self.lengths[index] * SPACE
                
                yield name

            
                 
def constructTopLine(names):
    for name in names[:-1]:
        if name.isspace():
            yield SPACE * (len(name) + 1)
        else:
            yield HORIZONTAL_LINE * (len(name) + 1)
    
    lastName = names[-1]

    if lastName.isspace():
        yield SPACE * (len(lastName) + 2)
    else:
        yield HORIZONTAL_LINE * (len(lastName) + 2)

@returnList
def constructContentLine(names):
    yield SPACE if names[0].isspace() else CENTER_VERTICAL_LINE

    for i, name in enumerate(names[:-1]):
        name = names[i]

        if name.isspace():
            yield len(name) * SPACE

            if names[i + 1].isspace():
                yield SPACE
            else:
                yield CENTER_VERTICAL_LINE
        else:
            yield name
            yield CENTER_VERTICAL_LINE 

    yield names[-1]

    yield SPACE if names[-1].isspace() else CENTER_VERTICAL_LINE
        

def main():
    layer1 = createLayer(ranges=[(0,0),(1,1),(2,2)],
                         names=['First Name', 'Second Name', 'Favourite Color'])
    layer1 = createLayer(ranges=[(0,0),(1,1),(2,2), (3,3)],
                         names=['          ', 'Second Name', '               ', 'adaad'])
    layer2 = createLayer(ranges=[(0,0),(1,1),(2,2), (3,3)],
                         names=['First', 'Second Name Name', 'Favourite Color', 'adada'])
    
    lengths1 = layer1.getLengths()
    names1 = layer1.getNames()

    lengths2 = layer2.getLengths()
    names2 = layer2.getNames()

    stringTableMatrix = [
        constructTopLine(names1),
        constructContentLine(names1),
        constructTopLine(names2),
        constructContentLine(names2),
        constructTopLine(names2)
    ]

    wholeString = NEW_LINE.join(listToString(row) for row in stringTableMatrix)

    print(wholeString)

def main2():
    layer1 = createLayer(ranges=[(0,0),(1,1),(2,2)],
                         names=['First Name', 'Second Name', 'Favourite Color'])
    a = ContentLineBuilder(layer1.getNames(), layer1.getLengths()).construct()
    print(a)