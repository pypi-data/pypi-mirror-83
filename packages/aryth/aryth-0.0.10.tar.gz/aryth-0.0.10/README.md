## aryth
##### numerical & statistics functions

### Usage
```python
from aryth.bound_vector import max_by, min_by

cities = [
    'jakarta',
    'bern',
    'san fransisco',
    '',
    'paris',
]
print(max_by(cities, len))
print(min_by(cities, len))
```