PARAM_NAME = '__param__'

class IndexedMetaclass(type):
    """
    Allows classes to be specialized with a parameter that is unique to that
    specific class object.

    ! Parameter must be hashable

    Not specifying/tracking a parameter defaults to tracking `None`. This means
    that `SomeType == SomeType[None]`.
    """

    # Non-specialized base classes (Arr, Str, Vec).
    # The data to construct the class itself is stored so that specializations
    # can add the tracked parameter. These are not useable types but the
    # constituent parts of a given type.
    tracked_base_types: dict[str, tuple[list[type], dict[str, object]]] = {}

    # Specializations have to be tracked separately because there could be many
    # of them (Arr[1], Str[1], Vec[1]). These are instantiated, usable, and
    # specialized types featuring a tracked parameter.
    tracked_base_type_specializations: dict[tuple[type, object], type] = {}

    def __new__(cls, name, bases, dict_):
        qualified_name = f'{dict_["__module__"]}.{dict_["__qualname__"]}'

        # Register the base type when it is defined using `class` keyword
        cls.tracked_base_types[qualified_name] = bases, dict_

        # Newly defined classes with `class` keyword are equivalent to:
        # `TheType[None]`.
        # The temporary type is exactly equivalent to the raw class definition
        # in Python source but it is discarded here since non-specialized types
        # are tracked as having a `None` specialized parameter.
        temporary_type = super().__new__(cls, name, bases, dict_)

        default_param = None  # Purposely None to signify it's not specialized

        # In theory, superclasses could include several specializations. Use the
        # closest ancestor
        for base in bases:
            for base_class in reversed(base.mro()):
                if isinstance(base_class, IndexedMetaclass):
                    default_param = getattr(base, PARAM_NAME)

        # Calls `IndexedMetaclass.__getitem__`
        return temporary_type[default_param]

    def __getitem__(self, param):
        """
        Create unique class (not instance) with custom parameter.

        If this method is called several times with the same specialization, it
        will return the cached specialized base type.
        """

        assert hasattr(param, '__hash__'), f'Unhashable type {type(param)}'

        qualified_name = f'{self.__module__}.{self.__qualname__}'
        lookup = qualified_name, param

        # Don't keep constructing new types from the same parameter hash
        if lookup in self.tracked_base_type_specializations:
            return self.tracked_base_type_specializations[lookup]

        bases, dict_ = self.tracked_base_types[qualified_name]

        # Return a newly constructed class object modified with the parameter
        new_class = super().__new__(
            self.__class__,
            self.__name__,
            bases,

            # Modifies the class definition to include the parameter
            {PARAM_NAME: param} | dict_
        )

        # Cache the new definition
        self.tracked_base_type_specializations[lookup] = new_class

        return new_class

    def __str__(self):
        param = getattr(self, PARAM_NAME)
        return f'{self.__qualname__}[{"" if param is None else param}]'

    def __repr__(self):
        return str(self)

    def __format__(self, _format):
        return str(self)


class IndexedClass(metaclass=IndexedMetaclass):
    """
    Example Usage:

    >>> class Vec(metaclass=IndexedMetaclass):
    ...     "This is equivalent to below"

    >>> class Vec:
    ...     "This is exactly the same as above"
    ...     __metaclass__ = IndexedMetaclass

    >>> class Vec(IndexedClass):
    ...     "Has some conveniences, but otherwise is identical to the above"

    >>> Vec[1] == Vec[1]
    True

    >>> Vec.__param__

    >>> Vec[1].__param__
    1

    >>> Vec[1, 2, 3].__param__
    (1, 2, 3)
    """

    def __str__(self):
        return (
            f'<{type(self).__module__}.{type(self)} object at {id(self):#018X}>'
        )

    def __repr__(self):
        return str(self)

    def __format__(self, _format):
        return str(self)
