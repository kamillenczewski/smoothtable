from typing import Iterable

from .color_condition import ColorCondition
from .extra_variable import ExtraVariable
from .utils import columnsToRowsGen, rowsToColumns, returnList, columnsToRows
from .constants import COLORS, TEXT_STYLES




class ColorItem:
    def __init__(self, color=None, style=None):
        self.color = color
        self.style = style

    def isEmpty(self):
        return not self.color and not self.style

def paintString(string, color, style):
    color = COLORS[color] if color else ""
    style = TEXT_STYLES[style] if style else ""

    string = color + style + "{}\033[0m".format(string)

    return string

@returnList
def emptyColumnMesh(size):
    for _ in range(size):
        yield ColorItem()

@returnList
def emptyColumnsMesh(columnsAmount, columnSize):
    for _ in range(columnsAmount):
        yield emptyColumnMesh(columnSize)


class Painter:
    def __init__(self, colorConditions: Iterable[ColorCondition]):
        self.colorConditions = colorConditions        

    @returnList
    def createColumnColorMesh(self, condition, array):
        extra = ExtraVariable()

        if condition.initMethod:
            condition.initMethod(array, extra)
            
        for index, item in enumerate(array):
            args = [locals()[argName] for argName in condition.args]

            if condition.method(*args):
                yield ColorItem(condition.color, condition.style)
            else:
                yield ColorItem()

    @returnList
    def createColorMesh(self, condition, columns):
        for column in columns:
            yield self.createColumnColorMesh(condition, column)

    @returnList
    def createColorMeshes(self, arrays):
        for condition in self.colorConditions:
            if condition.type == 'row':
                rows = columnsToRows(arrays)
                mesh = self.createColorMesh(condition, rows)
                mesh = rowsToColumns(mesh)
                yield mesh
            
            if condition.type == 'column':
                yield self.createColorMesh(condition, arrays)
            
    def mergeMeshes(self, meshes, columnsAmount, columnSize):
        finalMesh = emptyColumnsMesh(columnsAmount, columnSize)

        for mesh in meshes:
            for column, finalColumn in zip(mesh, finalMesh):
                for item, finalItem in zip(column, finalColumn):
                    if item.isEmpty():
                        continue

                    if not finalItem.color:
                        finalItem.color = item.color
                    
                    if not finalItem.style:
                        finalItem.style = item.style
        
        return finalMesh

    def createMesh(self, columns, columnsAmount, columnSize):
        meshes = self.createColorMeshes(columns) 
        finalMesh = self.mergeMeshes(meshes, columnsAmount, columnSize)
        return finalMesh


    @returnList
    def applyMeshToColumn(self, column, columnMesh):
        for stringItem, colorItem in zip(column, columnMesh):
            yield paintString(stringItem, colorItem.color, colorItem.style)

    @returnList
    def applyMesh(self, columns, mesh):
        for column, columnMesh in zip(columns, mesh):
            yield self.applyMeshToColumn(column, columnMesh)


def main():
    cond = ColorCondition(
        type='column',
        args='item',
        method=lambda item: len(item) == 3,
        color='red',
        style='bold'
    )

    columns = [["asas", 'dajkijda', '1ga']]

    painter = Painter([cond])
    painted = painter.paint(columns)

    print(painted)

if __name__ == '__main__':
    main()