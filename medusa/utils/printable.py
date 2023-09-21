class Printable:
    """A mixin class for objects that can be represented as strings and have a 
    printable representation.

    This class provides default implementations for the `__str__` and `__repr__` 
    methods, which return a string representation of the object's class name and its 
    attributes.
    """

    def __repr__(self) -> str:
        """Return a string representation of the object suitable for debugging.

        Returns:
            `str`: A string containing the class name and the object's attributes.
        """
        return self.__str__()

    def __str__(self) -> str:
        """Return a string representation of the object.

        Returns:
            `str`: A string containing the class name and the object's attributes.
        """

        return f"{self.__class__.__name__}({vars(self)})"
