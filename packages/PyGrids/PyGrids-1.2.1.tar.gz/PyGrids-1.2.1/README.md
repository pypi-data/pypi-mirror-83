# PyGrids

## Description
PyGrids is an module for storing and manipulating spreadsheet-like or grid-like information in python.
It also uses numpy to speed up array operations.

## Example
```py
from grids import Grid

grid = Grid(5,3) # Create an empty 5x3 grid.

print(grid.get_cell(5,3)) # -> ∅ None
print(grid.get_cell(3,1)) # -> ∅ None

grid.update_cell(5,3,'Foo')
grid.update_cell(3,2,'Bar')

print()
print(grid.view())
```
Will output...
```py
∅ 
∅

∅      ∅      ∅      ∅      ∅     
∅      ∅      'Bar'  ∅      ∅     
∅      ∅      ∅      ∅      'Foo' 
```

## Installation
```bash
$ pip install pygrids
```

## ``Grid`` Usage
Here's how you can use PyGrids.

### Using cells
**Getting cells**
```py
grid.get_cell(<x>, <y>)
```

**Updating cells**
```py
grid.update_cell(<x>, <y>, <new_value>)
```

**Overviewing cells**
```py
print(grid.view())
```

**Iterating through cells**
> By Columns
```py
for column in grid.y_by_x():
    for cell in column:
        print(x)
```
> By Rows
```py
for row in grid.x_by_y():
    for cell in row:
        print(y)
```

### Saving `Grid`s
You can save your grids by using their built-in ``save()`` method.
```py
# Saves by default to grid1.dat or grid2.dat if that's taken or grid3.dat if grid2.dat it taken, etc.
grid.save()
# Or you can specify a specify a specific filename
grid.save(filename='mygrid.dat')
```

### Loading `Grid`s from file
You can also load your grids into python by using `Grid`'s static ``load()`` method like so.
```py
grid = Grid.load('mygrid.dat')
```

## ``GridLog``'s
Each grid object tracks when it's methods are used and logs them to it's unique ``GridLog`` object. Let's take a look from out first example, what it's log would look like.
```py
print(grid.log)
```
Looks something like
```py
[GridLog created at [2020-10-21 20:30:11.230139]]:
-> [GET_CELL] (5, 3) at [2020-10-21 20:30:11.230171]
-> [GET_CELL] (3, 1) at [2020-10-21 20:30:11.230233]
-> [UPDATE_CELL] (5, 3, 'Foo') at [2020-10-21 20:30:11.230270]
-> [UPDATE_CELL] (3, 2, 'Bar') at [2020-10-21 20:30:11.230286]
-> [LOG_VIEW] () at [2020-10-21 20:30:11.230401]
```

## ``MultiDimensionalArray``'s
Unlike grids, which are constrained to only 2 dimensions, `MultiDimensionalArray`s support arrays of any shape.

```py
from grids import MultiDimensionalArray

myshape = [3,2,4,5]

array = MultiDimensionalArray(myshape)
```

Keep reading for how to use it

## MultiDimensionalArray Usage
Here's a few example's on how use MultiDimensionalArray's

### Updating and Getting Cells
```py
target_coord = [1,2,3,4]

array.update_cell(target_coord, 'Foo')

print(array.get_cell(target_coord)) # Foo
```

## License
This software is licensed by an MIT License.