from indexed_meta import IndexedMetaclass, IndexedClass, get_param


def test_class_registration():
    class Vec:
        assert "Verify metaclass variable can be specified in class body"
        __metaclass__ = IndexedMetaclass

    class Vec(metaclass=IndexedMetaclass):
        assert "Verify metaclass parameter works"

    class Vec(IndexedClass):
        assert "Verify class-based inheritance works"


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


def test_caching():
    class A(metaclass=IndexedMetaclass):
        ""

    alias_to_original = A

    class A(IndexedClass):
        pass

    assert alias_to_original == A, (
        'IndexedClass & IndexedMetaclass classes should refer to same type'
    )

    assert str(A) ==  str(alias_to_original), (
        'IndexedClass & IndexedMetaclass classes should refer to same type'
    )


def test_inherit_param():
    class A(IndexedClass): ...
    class B(A): ...

    assert B.__param__ is None
    assert B[-1].__param__ == -1, 'Subclass failed to specialize'

    class C(A[-1]): ...

    assert C.__param__ == -1, 'Did not inherit param'


def test_get_param():
    class A(IndexedClass): ...

    assert get_param(A) is None
    assert get_param(A[1]) == 1
    assert get_param(A[A]) == A
    assert get_param(A[A[A]]) == A[A]
