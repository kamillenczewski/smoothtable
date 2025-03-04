from smoothtable.smooth_table_builder import SmoothtableBuilder
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


table = (SmoothtableBuilder()
    .putLabelLayer({'0-3': 'Identification', '3-5': 'Other'})
    .putLabelLayer({'0': 'Id', '1': 'First Name', '2': 'Last Name', '3': 'Favourite Color', '4': "Car brand"})

    .addColumn(['1', '2', '3'])
    .addColumn(['Kamil', 'Anastazja', 'Karolina'])
    .addColumn(['Lenczewski', 'Kasprzyk', 'Olawska'])
    .addColumn(['Blue', 'Red', 'Yellow'])
    .addColumn(['R1', 'R1', 'V1'])

    .addColorCondition(condition1)
    .addColorCondition(condition2)
    .addColorCondition(condition3)

    .build())


print(table)