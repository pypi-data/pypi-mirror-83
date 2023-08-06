# filterlib

A filter library for python by Fabian Becker.

## What for?

With a `Filter` object you can easily check for attributes of an object to equal a given value.

## Usage

### How to create a filter

#### Create a filter using __init__()

Both attributes are optional.

`operator: str = "AND"` (`"AND"` or `"OR"`) sets the logical operator for the filter (checks all or any attributes). 

`allow_missing_attributes: bool = False` sets the tolerance for missing attributes. If set to true it will skip if the attribute is missing in the object to check.

#### Create a filter from its representation

The return value of a filters `__repr__` attribute can be used to store and later on recreate a filter using `filter_from_repr`

```python
from filterlib import Filter, filter_from_repr

f = Filter()

print(f == filter_from_repr(repr(f)))
# f and filter_from_repr(f.__repr__()) is the same
```

#### Additional attributes

The attribute a filter checks for are variable
```python
from filterlib import Filter
# Use the following systax:
f = Filter(<Optional[attibute name]><attributes magic method>=<value>)

# For example:
f = Filter(a__eq__=1)

# You can also use multiple attributes:
f = Filter(b__lte__=5,
           c__gt__=2)

# Or check for objects themselves
Filter(__eq__="Hello World!") == "Hello World!"
```

### Use a filter

Make sure you use the filters `__eq__` attribute.

```python
# Make sure you use
Filter() == x
# instead of
x == Filter()
```

## Example
```python
from filterlib import Filter
from typing import Optional


class Person:
    def __init__(self, 
                 name: str,
                 age: int,
                 best_friend: Optional[Person] = None):
        self.name = name
        self.age = age
        self.best_fiend = best_friend


f = Filter(name__eq__="John")
p = Person(name="John", age=35)
print(f == p)
# True

f = Filter(name__ne__="John")
p = Person(name="John", age=35)
print(f == p)
# False

f = Filter(name__eq__="John", age__lte=40)
p = Person(name="John", age=35)
print(f == p)
# True

f = Filter(name__eq__="John", age__lte=20)
p = Person(name="John", age=35)
print(f == p)
# False

f = Filter(operator="OR",
           name__eq__="John", 
           age__lte=20)
p = Person(name="John", age=35)
print(f == p)
# True

p = Person(name="John",
           age=35,
           best_friend=Person(name="Thomas",
                              age=36))
f = Filter(best_friend__name__eq__="Thomas", 
           age__lte=40)
print(f == p)
# True
```

## SQL compatability
You can use filters for sql statements
```python
from filterlib import Filter
import sqlite3

db = sqlite3.connect("myDB.sqlite")
db.execute("CREATE TABLE users(id, name)")
f = Filter(id__eq__=1)
db.execute(f"SELECT name FROM users WHERE {f}")
```