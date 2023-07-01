
# TODO(pbz): Prevent regular instantiation with __init__ (List[3] vs List ...)

class IndexedMeta(type):
    """
    Allows classes to be specialized with a parameter that is unique to that
    specific class object.
    """

    # Non-specialized base classes (Arr vs Arr[length])
    tracked_base_types: dict[str, tuple[list[type]], dict[str, object]] = {}

    # Specializations have to be tracked separately because there could be many
    # of them (Arr[1], Arr[2], Arr[3])
    tracked_base_type_specializations: dict[tuple[type, object], type] = {}

    def __new__(cls, name, bases, dict_):
        # Register the base type when it is defined using `class` keyword
        cls.tracked_base_types[name] = bases, dict_

        # Return the newly constructed class object unmodified
        return super().__new__(cls, name, bases, dict_)

    def __getitem__(self, param):
        """
        Create unique class (not instance) with custom parameter.

        If this method is called several times with the same specialization, it
        will return the cached specialized base type.
        """

        assert hasattr(param, '__hash__'), f'Unhashable type {type(param)}'

        lookup = self.__name__, param

        # Don't keep constructing new types from the same parameter hash
        if lookup in self.tracked_base_types:
            return self.tracked_base_types[lookup]

        bases, dict_ = self.tracked_types[self.__name__]

        # Return a newly constructed class object modified with the parameter
        new_class = super().__new__(
            self.__class__,
            self.__name__,
            bases,

            # Modifies the class definition to include the parameter
            dict(param=param, **dict_)
        )

        # Cache the new definition
        self.tracked_base_types[lookup] = new_class

        return new_class

    def __str__(self):
        return f'{self.__name__}[{getattr(self, "param", "")}]'

    def __repr__(self):
        return str(self)

    def __format__(self, _format):
        return str(self)
