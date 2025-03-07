<img width="538" alt="image" src="https://github.com/user-attachments/assets/62819fb5-62ca-49cc-8482-2c9f5f4c3a8c" /># smoothtable

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

![Example output](https://github.com/kamillenczewski/smoothtable/blob/main/example.png)

## 🏃 Usage

This section explains how to create table showed above // change change

Needed dependencies:

```python
from smoothtable.smooth_table_builder import SmoothtableBuilder
from smoothtable.color_condition import ColorCondition
```

`ColorCondition` stores information about how a color mask should be created:
- type (`row` or `column`) - depends on which type of array you want to iterate through
- args (`index` `item` `array` or `extra`) - you can choose among them to construct condition method like you want
- method - takes arguments from `args` and returns boolean value
- color
- style

Let's create 3 conditions:
- `condition1` - red color and bold style are assigned to every element in row which second item ends with letter 'a'.
- `condition2` - yellow color and bold style are assigned to every element in column which first item is equal to "Kamil".
- `condition3`
    - explanation of args that are passed and what they do

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
Subsequently, use `Painter` class to combine `ColorCondition` objects.

**WARNING!** Order of passing conditions does matter (first condition is more important than the second one).


Creating table

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
```
