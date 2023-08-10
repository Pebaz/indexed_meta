# indexed_meta

Python metaclass with support for per-class specialization via an index method.

Adds a `__param__` field to classes programmatically so that you can store a
static field on them without having to define a new class and without having to
use a new name.

```python
from indexed_meta import IndexedMetaclass  # Base type but either will work fine
from indexed_meta import IndexedClass  # Convenience type. Fixes repr(), str()

class Vec(IndexedClass):
    def show(self):
        # This is the value-add for this library. Use __param__ as you see fit.
        # It is different per specialized class but the exact same when param is
        # the same: Vec[1] == Vec[1]; Vec[1] != Vec[2]
        print(self.__param__)

v1 = Vec[3]()
v1.show()  # Prints `3`

Vec[1], Vec[2], Vec[3], Vec[1, 2, 3], Vec[frozenset([1, 2, 3])]

# It's possible to override the default __param__ of None by inheriting from a
# specialized class:
class Vec(metaclass=IndexedMetaclass):
    ...

class Vec4(Vec[4]):
    ...

assert Vec4.__param__ == 4  # Normally it would be `None`
```
