"""Bit Position Member class."""

from .bitfield import BitField


class BitPos:
    """A member class representing a pit position for use in a BitField class."""

    def __init__(self, idx: int) -> None:
        """Initialize BitPos."""
        super().__init__()
        self._idx = idx

    def __get__(self, instance, owner=None):
        """Implement get descriptor."""
        if not isinstance(instance, BitField):
            raise TypeError("BitPos only intended for use on BitField classes.")
        return instance[self.idx]

    def __set__(self, instance, value) -> None:
        """Implement set descriptor."""
        if not isinstance(instance, BitField):
            raise TypeError("BitPos only intended for use on BitField classes.")
        instance[self.idx] = value

    @property
    def idx(self) -> int:
        """Return read-only index value."""
        return self._idx
