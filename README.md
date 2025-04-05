My work was inspired by https://github.com/nirum/tableprint 

## 🔎 Table of Contents
-   [Installation](#%EF%B8%8F-installation)
-   [About](#%EF%B8%8F-about)
-   [Usage](#-usage)

## 🖥️ Installation
```
pip install smoothtable
```

## ⚛️ About 
`smoothtable` lets you display rows and columns in user-friendly style. 
Moreover, you can create color conditions using `ColorCondition` class to 
emphasize visibility of specific values in your data sets.


## 🏃 Usage

This section explains how to create table using this library

Needed dependencies:

```python
from smoothtable.smooth_table_builder import SmoothtableBuilder
from smoothtable.color_condition import ColorCondition
```

`ColorCondition` stores information about how a color mask should be created:
- type (`row` or `column`) - depends on which type of array you want your condition function to iterate through
- args (`index` `item` `array` or `extra`) - you can choose among them to construct condition method like you want
- method - takes arguments from `args` and returns boolean value
- color
- style

Let's create 3 conditions:
- `condition1` - red color and bold style are assigned to every element in row which second item ends with the letter 'a'.
- `condition2` - yellow color and bold style are assigned to every element in column which first item starts with the letter 'C'.
- `condition3` - green color is assigned to the all remaining data

```python
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
```

**WARNING!** Order of passing conditions does matter (first condition is more important than the second one).

To construct wanted table we must use class `SmoothtableBuilder`. 

Possible creation methods:
- `putLabelLayer` - takes dictionary with ranges and names of horizontal labels
- `addColumn` - adds column (remember to add proper amount of data each time)
- `addColorCondition` - apply our color condition to the table

```python
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

    .build())

print(table)
```

![Example output](https://github.com/kamillenczewski/smoothtable/blob/main/example.png)
