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
    method=lambda array: array[0].startswith('C'),
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
    .putLabelLayer({'0-2': 'All'})

    .putLabelLayer({'0-3': 'Identification', 
                    '3-5': 'Other'})
                    
    .putLabelLayer({'0': 'Id', 
                    '1': 'First Name', 
                    '2': 'Last Name', 
                    '3': 'Favourite Color', 
                    '4': "Favourite Car Brand"})

    .addColumn(['1', '2', '3', '4', '5', '6'])
    .addColumn(['Bernard', 'Greg', 'Diana', 'Sheila', 'Sophia', 'Rolf'])
    .addColumn(['Cress', 'Colon', 'Harrett', 'Hersey', 'Larson', 'Robinett'])
    .addColumn(['Blue', 'Red', 'Yellow', 'Red', 'Red', 'Blue'])
    .addColumn(['Tesla', 'Audi', 'Tesla', 'Toyota', 'Audi', 'Toyota'])

    .addColorCondition(condition2)
    .addColorCondition(condition1)
    .addColorCondition(condition3)

    .setLabelsAlignment('center')

    .build())

print(table)