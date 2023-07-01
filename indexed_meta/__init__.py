
class Sized(type):
    "Metaclass that allows index syntax to add integer size attribute per class"

    # For every class that has Sized as a metaclass, the base classes and dict
    # definition are stored here by class name so that a `size` static field can
    # be added onto it
    tracked_types: dict[str, tuple[list[type]], dict[str, object]] = {}

    # To prevent many same-sized duck types from being created, track each new
    # sized types by name and size
    tracked_sized_types: dict[tuple[type, int], type] = {}

    def __new__(cls, name, bases, dict_):
        cls.tracked_types[name] = bases, dict_

        # Returns exactly 1 unique type without a static `size` field so that
        # it can be used along with subscript syntax `[]` to produce any number
        # of subclasses that customize that size type
        return super().__new__(cls, name, bases, dict_)

    def __getitem__(self, size):
        """
        Create unique class (not instance) with custom size.

        If this method is called several times with the same size input, it will
        produce that many new classes.
        """

        lookup = self.__name__, size

        if lookup in self.tracked_sized_types:
            return self.tracked_sized_types[lookup]

        bases, dict_ = self.tracked_types[self.__name__]

        # This can return any number of new classes that are exact duck types of
        # the class originally stored in `tracked_types`. The difference is the
        # static field `size` that is customized in this method
        new_class = super().__new__(
            self.__class__,
            self.__name__,
            bases,

            # Make sure to add the static field here to prevent always having
            # the last known value being stored on the type
            dict(size=size, **dict_)
        )

        self.tracked_sized_types[lookup] = new_class

        return new_class

    def __str__(self):
        return f'{self.__name__}[{getattr(self, "size", "")}]'

    def __repr__(self):
        return str(self)

    def __format__(self, _format):
        return str(self)


# TODO(pbz): Can track anything that implements __hash__
# TODO(pbz): Prevent regular instantiation with __init__ (List[3] vs List ...)

class IndexedMeta(type):
    tracked_types: dict[str, tuple[list[type]], dict[str, object]] = {}
    tracked_sized_types: dict[tuple[type, int], type] = {}

    tracked_base_types = {}
    tracked_base_type_specializations = {}

    def __new__(cls, name, bases, dict_):
        cls.tracked_types[name] = bases, dict_

        return super().__new__(cls, name, bases, dict_)

    def __getitem__(self, size):
        """
        Create unique class (not instance) with custom size.

        If this method is called several times with the same size input, it will
        produce that many new classes.
        """

        lookup = self.__name__, size

        if lookup in self.tracked_sized_types:
            return self.tracked_sized_types[lookup]

        bases, dict_ = self.tracked_types[self.__name__]

        new_class = super().__new__(
            self.__class__,
            self.__name__,
            bases,

            dict(size=size, **dict_)
        )

        self.tracked_sized_types[lookup] = new_class

        return new_class

    def __str__(self):
        return f'{self.__name__}[{getattr(self, "size", "")}]'

    def __repr__(self):
        return str(self)

    def __format__(self, _format):
        return str(self)


