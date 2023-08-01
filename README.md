# indexed_meta

Python metaclass with support for per-class specialization via an index method.

```python
from indexed_meta import IndexedMetaclass  # Base type but either will work fine
from indexed_meta import IndexedClass  # Convenience type. Fixes repr(), str()


class Vec(metaclass=IndexedMetaclass):
    "This is equivalent to below"


class Vec:
    "This is exactly the same as above"
    __metaclass__ = IndexedMetaclass


class Vec(IndexedClass):
    "This class has some conveniences, but otherwise is identical to the above"



def test_class_specialization():
    class Vec(metaclass=IndexedMetaclass):
        assert "Verify metaclass parameter works"

    assert Vec == Vec[None], 'Non-specialized types should track None parameter'
    assert Vec[None] == Vec[None], 'Specialized types should be cached'
    assert Vec[1] != Vec[2], 'Specialized types should be different'

    class Vec(IndexedClass):
        assert "Verify class-based inheritance works"

    assert Vec == Vec[None], 'Non-specialized types should track None parameter'
    assert Vec[None] == Vec[None], 'Specialized types should be cached'
    assert Vec[1] != Vec[2], 'Specialized types should be different'


def test_no_aliasing():
    def example1():
        class A(IndexedClass):
            "First class named `A`"
        return A

    def example2():
        class A(IndexedClass):
            "Second class named `A` and should be distinct type"
        return A

    A1, A2 = example1(), example2()

    assert A1.__qualname__ != A2.__qualname__, (
        'Classes with same name from different scopes should be different'
    )

    assert A1 != A2, (
        'Classes with same name from different scopes should be different'
    )
s
```
