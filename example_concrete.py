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


table = createTable(
    columnLabels=[
        {'0-3': 'Identification', '3-5': 'Other'},
        {'0': 'Id', '1': 'First Name', '2': 'Last Name', '3': 'Favourite Color', '4': "Car brand"}
    ],
    columns=[
        ['1', '2', '3'],
        ['Kamil', 'Anastazja', 'Karolina'],
        ['Lenczewski', 'Kasprzyk', 'Olawska'],
        ['Blue', 'Red', 'Yellow'],
        ['R1', 'R1', 'V1']
    ]
)

print(table)