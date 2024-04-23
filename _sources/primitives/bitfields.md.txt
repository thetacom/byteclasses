# BitFields

A generic bitfield is a single byte primitive used for extracting bit values from a byte.

Bit values can be retrieved or set using the `get_bit(idx)` and `set_bit(idx, val)` methods respectively.

```python
bf = BitField()
bf.set_bit(0, 1)
bf.set_bit(1, True)
bf.get_bit(0)
```

The BitField class also support getting/setting bits by indexing on an instance.

```python
bf = BitField()
bf[2] = 1
bf[3] = True
```

Data can be accessed directly via the `.data` attribute.

```python
bf = BitField()
bf.data = b"\xFF"
```

## Custom BitFields

A custom `BitField` enables several unique features not available with a generic `BitField`.

1. The `BitField` class internally supports multiple bytes. The length of a `BitField` class can be adjusted by specifying a `byte_length` class attribute.
2. Individual bits can be named through the use of the `BitPos` typed class attributes. Adding these attributes provides an additional method for accessing bit values.

```python
from byteclasses.primitives import BitField, BitPos

class MyBitField(ByteField):
    """A two byte bit field with two named bit."""

    byte_length = 2

    first = BitPos(0)
    middle = BitPos(8, bit_width = 4)
    last = BitPos(15)

bv = MyBitField()
bv.first = 1
bv.middle = 0b1010
bv.last = True
```
