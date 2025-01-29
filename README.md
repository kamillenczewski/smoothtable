# smoothtable

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
Moreover you can create color conditions using `ColorCondition` class to 
emphasize visibility of specific values in your data sets

![Example output](https://github.com/kamillenczewski/smoothtable/blob/main/example.png)

## 🏃 Usage

This section explains how to create table showed above

Needed import statements

```python
from smoothtable.table import createTable
from smoothtable.color_condition import ColorCondition
from smoothtable.painter import Painter
```
`ColorCondition` stores information about how a mesh should be created:
- type (`row` or `column`) - depends on which type of array you want to iterate through
- args (`index` `item` `array` or `extra`) - you can choose among them to construct condition method like you want
- method - takes arguments from `args` and returns boolean value
- color (currently only `red`)
- style (currently only `bold`)

Let's create two conditions:
- `condition1` - red color and bold style are assigned to every element in row which second item ends with letter 'a'.
- `condition2` - yellow color and bold style are assigned to every element in column which first item is equal to "Kamil".

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
    method=lambda array: array[0] == 'Kamil',
    color='yellow',
    style='bold'
)
```
Subsequently, use `Painter` class to combine `ColorCondition` objects.

**WARNING!** Order of passing conditions does matter (first condition is more important than the second one).

```python
painter = Painter([condition1, condition2])
```

`createTable` method contains:
- columnLabels
- rowLabels
- rows or columns
- painter

```python
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
```
