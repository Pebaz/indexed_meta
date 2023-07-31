from indexed_meta import *

# class Vec(metaclass=IndexedMetaclass):
#     pass

class Vec(IndexedClass):
    pass

# print(Vec)
# print(Vec[1])
# print(Vec())
# print(Vec[1]())

# print('Deref:', Vec[1, 2].__param__)
# print('Deref:', Vec.__param__)
# print('Deref:', Vec[1]().__param__)
# print('Deref:', Vec().__param__)
# print('Deref:', *Vec[1, 2])
# print('True?', Vec == Vec[None])
print(Vec, Vec[None])

assert Vec == Vec[None]
