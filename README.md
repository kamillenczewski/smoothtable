# smoothtable

My work is inspired by https://github.com/nirum/tableprint 

## About 
`smoothtable` lets you display rows and columns in user-friendly style. 
Moreover you can create color conditions using `ColorCondition` class to 
emphasize visibility of specific values in your data sets

## Table of Contents
-   [About](#-about)


## 🏃 Usage

Importing needed stuff

```python
from table import createTable
from color_condition import ColorCondition, Painter
```

`ColorCondition` contains:
- type (`row` or `column`), depends on which type of array you want to iterate through
- args (`index` `item` `array` or `extra`), you can choose among them to construct condition method like you want
- method - function which takes arguments from `args` and returns boolean value
- color (currently only `red`)
- style (currently only `bold`)

```python
condition = ColorCondition(
    type='row',
    args='array',
    method=lambda array: array[1].strip().endswith('a'),
    color='red',
    style='bold'
)
```

`Painter` class combine `ColorCondition` objects and enables to paint strings

```python
painter = Painter([condition])
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
```

Table display

```python
print(table)
```
