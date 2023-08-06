## palett
##### pretty text for command line

### Usage
```python

from palett.fluo.fluo_vector import fluo_vector
from palett.presets import FRESH, PLANET

vectorCollection = [
    [],
    ['Xx', 'Yy', 'Zz', 'e', 'd', 'c', '-', '1', 2, 3],
    [1, 1, 2, 3, 5, []],
    ['a', 'b', 'c', 'd', 'e'],
    ['beijing', 'shanghai', 'wuhan', 'xiamen', 'changsha']
]


def test():
    COMMA_SPACE = ', '
    for vec in vectorCollection:
        fluoed = fluo_vector(vec, (FRESH, PLANET))
        print(f'[{COMMA_SPACE.join(fluoed)}]')


test()
```