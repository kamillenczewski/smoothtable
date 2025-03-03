from smoothtable.table import SmoothtableBuilder
from smoothtable.color_condition import ColorCondition


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

table = SmoothtableBuilder()\
    .putLabelLayer({'0-3': 'Identification', '3-5': 'Other'})\
    .putLabelLayer({'0': 'Id', '1': 'First Name', '2': 'Last Name', '3': 'Favourite Color', '4': "Car brand"})\
    .setColumns([['1', '2', '3'],
                 ['Kamil', 'Anastazja', 'Karolina'],
                 ['Lenczewski', 'Kasprzyk', 'Olawska'],
                 ['Blue', 'Red', 'Yellow'],
                 ['R1', 'R1', 'V1']])\
    .build()

print(table)