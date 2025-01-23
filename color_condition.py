from typing import Iterable

class ColorCondition:
    ARGS = ('item', 'index', 'array', 'extra')
    ARGS_TYPES = (str, Iterable)
    CONDITION_TYPES = ('row', 'column')

    def __init__(self, type, method, args, color, style, initMethod=None):
        self.type = self.validateType(type)
        self.method = method
        self.args = self.interprateArgs(args)
        self.initMethod = initMethod
        self.color = color
        self.style = style
        
    def interprateArgs(self, args):
        assert type(args) in self.ARGS_TYPES, f"Invalid args type: '{type(args)}'!"

        if isinstance(args, str):
            args = args.split()

        assert all((arg in self.ARGS for arg in args)), f"Invalid args passed: {args}. Possible args: {self.ARGS}"
    
        return args

    def validateType(self, type):
        assert type in self.CONDITION_TYPES

        return type

class ExtraVariable:
    def __init__(self, obj=None):
        self.obj = obj


def getColor(name):
    match(name):
        case 'red':
            return '\033[31m'

def getStyle(name):
    match(name):
        case 'bold':
            return '\033[01m'

def paintString(string, color, style):
    color = getColor(color)
    style = getStyle(style)
    string = color + style + "{}\033[0m".format(string)
    return string


def columnsToRowGen(columns, rowIndex):
    for column in columns:
        yield column[rowIndex]

def columnsToRow(columns, rowIndex):
    return list(columnsToRowGen(columns, rowIndex))

def columnsToRowsGen(columns):
    for rowIndex in range(len(columns[0])):
        yield columnsToRow(columns, rowIndex)

def columnsToRows(columns):
    return list(columnsToRowsGen(columns))



def rowsToColumnGen(rows, columnIndex):
    for row in rows:
        yield row[columnIndex]

def rowsToColumn(rows, columnIndex):
    return list(rowsToColumnGen(rows, columnIndex))

def rowsToColumnsGen(rows):
    for rowIndex in range(len(rows[0])):
        yield rowsToColumn(rows, rowIndex)

def rowsToColumns(rows):
    return list(rowsToColumnsGen(rows))



class Painter:
    def __init__(self, colorConditions: Iterable[ColorCondition]):
        self.colorConditions = colorConditions

    def paintArray(self, array, condition: ColorCondition):
        extra = ExtraVariable()

        if condition.initMethod:
            condition.initMethod(array, extra)
            
        for index, item in enumerate(array):
            args = [locals()[argName] for argName in condition.args]

            if condition.method(*args):
                yield paintString(item, condition.color, condition.style)
            else:
                yield item           
    

    def paintColumns(self, columns, condition: ColorCondition):
        for column in columns:
            yield list(self.paintArray(column, condition))

    def paintRows(self, rows, condition: ColorCondition):
        for row in rows:
            yield list(self.paintArray(row, condition))


    def paint(self, columns):
        for condition in self.colorConditions:
            match(condition.type):
                case 'column':
                    columns = list(self.paintColumns(columns, condition))
                case 'row':
                    rows = columnsToRowsGen(columns)
                    rows = list(self.paintRows(rows, condition))
                    columns = rowsToColumns(rows)

        return columns

def main():
    cond = ColorCondition(
        type='row',
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