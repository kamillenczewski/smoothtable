from smoothtable.table import createTable
from smoothtable.color_condition import ColorCondition
from smoothtable.painter import Painter

condition1 = ColorCondition(
    type='row',
    args='array',
    method=lambda array: array[1][-1] == 'a',
    color='red',
    style='bold'
)

condition2 = ColorCondition(
    type='column',
    args='array',
    method=lambda array: array[0] == 'Kamil',
    color='yellow',
    style='bold'
)
condition3 = ColorCondition(
    type='row',
    args='array',
    method=lambda array: True,
    color='green',
    style='bold'
)


painter = Painter([condition1, condition2, condition3])

table = createTable(
    columnLabels=['Id', 'First name', 'Last name', 'Favourite Color'],
    rowLabels=['Row1', 'Row2', 'Row3', 'Row4', 'Row5'],
    rows=[
        ["1", 'Kamil', 'Lenczewski', 'Blue'],
        ["2", 'Anastazja', 'Kasprzyk', 'Red'],
        ["3", 'Karolina', 'Olawska', 'Black'],
        ["4", 'Adam', 'Lewandowski', 'Black'],
        ["5", 'Hania', 'Granat', 'Red']
    ],
    painter=painter
)

print(table)