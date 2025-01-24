from table import createTable
from color_condition import ColorCondition
from painter import Painter

# TO DO
# priorities for conditions to have control
# on which condition is more important than the other one

# Painter.paint -> createPaintMesh -> array which has color is speicfic positions
# and then we can jsut concat it so the condtion method will iterate through real objects
# not strings

# add possibility to create table with labels only in specfic location
# for example having columns id, name, fcolor we want to display
# id column but not the label for it

condition1 = ColorCondition(
    type='row',
    args='array',
    method=lambda array: array[1].strip().endswith('a'),
    color='red',
    style='bold'
)

condition2 = ColorCondition(
    type='column',
    args='array',
    method=lambda array: array[0].strip() == 'Kamil',
    color='yellow',
    style='bold'
)


painter = Painter([condition1, condition2])

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