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
    args='',
    method=lambda : True,
    color='green',
    style='bold'
)


painter = Painter([condition1, condition2, condition3])

# TO DO
# Change constants to maje them one char because 
# otherwise it is hard to understand what is actually going on here

# 'Id', 'First name', 'Last name'Favourite Color
table = createTable(
    columnLabels={'1-4': 'Identification', '6-8': 'Favourite Color', '10-10': "AHA"},
    columns=[
        ['1', '2', '3'],
        ['Kamil', 'Anastazja', 'Karolina'],
        ['Lenczewski', 'Kasprzyk', 'Olawska'],
        ['Blue', 'Red', 'Yellow'],
        ['R1', 'R1', 'V1'],
        ['R1', 'R1', 'V1'],
        ['R1', 'R1', 'V1'],
        ['R1', 'R1', 'V1'],
        ['R1', 'R1', 'V1'],
        ['R1', 'R1', 'V1']
    ],
    painter=painter
)

print(table)