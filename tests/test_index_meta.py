from indexed_meta import IndexedMetaclass, IndexedClass

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
