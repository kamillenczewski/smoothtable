from table import createTable
from color_condition import ColorCondition, Painter

condition = ColorCondition(
    type='row',
    args='array',
    method=lambda array: array[1].strip().endswith('a'),
    color='red',
    style='bold'
)
painter = Painter([condition])

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

# Painter.paint -> createPaintMesh -> array which has color is speicfic positions
# and then we can jsut concat it so the condtion method will iterate through real objects
# not strings

print(table)