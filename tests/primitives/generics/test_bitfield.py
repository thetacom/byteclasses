"""Unit tests for byteclasses bitfield primitive type."""

import pytest

from byteclasses.types.primitives.bitfield import BitField, BitPos, bitpos2mask, mask2bitpos


class TestBitField(BitField):
    """A custom BitField class for testing."""

    __test__ = False

    byte_length = 2
    first_bit = BitPos(0)
    middle_bit = BitPos(8, bit_width=4)
    last_bit = BitPos(15)


def test_generic_bitfield_creation():
    """Create generic bitfield."""
    bf = BitField()
    assert bf.bit_length == 8
    assert len(bf) == 1
    assert bf.data == b"\x00"


def test_generic_bitfield_creation_with_valid_data():
    """Create generic bitfield with valid data."""
    bf = BitField(data=b"\xff")
    assert bf.data == b"\xff"
    assert all(bf.flags) is True


def test_generic_bitfield_creation_with_invalid_data():
    """Create generic bitfield with invalid data."""
    with pytest.raises(ValueError):
        _ = BitField(data="\xff\xff")


def test_generic_bitfield_value_property():
    """Create generic bitfield value property."""
    bf = BitField(data=b"\xff")
    assert bf.data == b"\xff"
    assert isinstance(bf.value, tuple)
    assert bf.value == tuple(True for _ in range(bf.bit_length))


def test_generic_bitfield_value_property_assignment_with_bool():
    """Create generic bitfield value property assignment with bool."""
    bf = BitField()
    assert bf.data == b"\x00"
    bf.value = True
    assert bf.data == b"\xff"
    bf.value = False
    assert bf.data == b"\x00"


def test_generic_bitfield_value_property_assignment_with_dict():
    """Create generic bitfield value property assignment with dict."""
    bf = BitField()
    assert bf.data == b"\x00"
    bf.value = tuple(True for _ in range(bf.bit_length))
    assert bf.data == b"\xff"
    bf.value = tuple(False for _ in range(bf.bit_length))
    assert bf.data == b"\x00"


def test_generic_bitfield_value_property_assignment_with_iterable():
    """Create generic bitfield value property assignment with iterable."""
    bf = BitField()
    bf.value = {1: True, 3: True, 5: True, 7: True}
    assert bf.data == b"\xaa"
    bf.value = {1: False, 3: False, 5: False, 7: False}
    assert bf.data == b"\x00"


def test_generic_bitfield_value_property_assignment_with_invalid_type():
    """Create generic bitfield value property assignment with invalid type."""
    bf = BitField()
    with pytest.raises(NotImplementedError):
        bf.value = "invalid"


def test_bitfield_get_bit():
    """Test BitField `get_bit` method."""
    bf = BitField()
    assert bf.get_bit(0) is False
    bf.data = b"\x01"
    assert bf.get_bit(0) is True
    with pytest.raises(IndexError):
        _ = bf.get_bit(8)


def test_bitfield_set_bit():
    """Test BitField `set_bit` method."""
    bf = BitField()
    bf.set_bit(0, True)
    assert bf.data == b"\x01"
    bf.data = b"\x00"
    bf.set_bit(0, 1)
    assert bf.data == b"\x01"
    with pytest.raises(IndexError):
        bf.set_bit(8, True)


def test_bitfield_clear_bit():
    """Test BitField `clear_bit` method."""
    bf = BitField(data=b"\xff")
    bf.clear_bit(0)
    assert bf.data == b"\xfe"


def test_bitfield_get_bit_index():
    """Get bit value by index."""
    bf = BitField()
    assert bf.data == b"\x00"
    assert bf[0] is False
    assert bf[-1] is False
    bf.data = b"\x81"
    assert bf[0] is True
    assert bf[-1] is True


def test_bitfield_index_out_of_bounds():
    """Create generic bitfield."""
    bf = BitField()
    with pytest.raises(IndexError):
        print(bf[8])
    with pytest.raises(IndexError):
        bf[8] = 1


def test_bitfield_get_bit_values_with_index_slice():
    """Get bit values with index slice."""
    bf = BitField(data=b"\x55")  # 0b01010101
    assert bf[:] == [True, False, True, False, True, False, True, False]
    assert bf[::2] == [True, True, True, True]
    assert bf[1:] == [False, True, False, True, False, True, False]
    assert bf[1:7] == [False, True, False, True, False, True]
    assert bf[::-1] == [False, True, False, True, False, True, False, True]

    assert bf[:-1:] == []  # Expected behavior?


def test_bitfield_set_bit_values_with_index_slice():
    """Set bit values with index slice."""
    bf = BitField()
    bf[:] = True
    assert bf.data == b"\xFF"
    bf.data = b"\x00"
    bf[::2] = True
    assert bf.data == b"\x55"
    bf.data = b"\x00"
    bf[1:] = True
    assert bf.data == b"\xfe"
    bf.data = b"\x00"
    bf[1:7] = True
    assert bf.data == b"\x7e"
    bf.data = b"\x00"
    bf[::-1] = True
    assert bf.data == b"\xff"
    bf.data = b"\x00"

    bf[:-1:] = True  # Expected behavior?
    assert bf.data == b"\x00"


def test_bitfield_set_bit_values_with_index_slice_and_sequence():
    """Set bit values with index slice and sequence."""
    bf = BitField()
    bf[:] = [True, True, True, True, True, True, True, True]
    assert bf.data == b"\xFF"
    bf.data = b"\x00"
    bf[::2] = [True, True, True, True, True, True, True, True]
    assert bf.data == b"\x55"
    bf.data = b"\x00"
    bf[1:] = [True, True, True, True, True, True, True, True]
    assert bf.data == b"\xfe"
    bf.data = b"\x00"
    bf[1:7] = [True, True, True, True, True, True, True, True]
    assert bf.data == b"\x7e"
    bf.data = b"\x00"
    bf[::-1] = [True, True, True, True, True, True, True, True]
    assert bf.data == b"\xff"
    bf.data = b"\x00"

    bf[:-1:] = [True, True, True, True, True, True, True, True]  # Expected behavior?
    assert bf.data == b"\x00"


def test_bitfield_get_bit_values_with_invalid_index():
    """Get bit values with invalid index."""
    bf = BitField()
    with pytest.raises(NotImplementedError):
        _ = bf["invalid"]


def test_bitfield_set_bit_values_with_invalid_index():
    """Set bit values with invalid index."""
    bf = BitField()
    with pytest.raises(NotImplementedError):
        bf["invalid"] = True


def test_bitfield_set_bit_index_with_bool():
    """Set bit value by index using boolean value."""
    bf = BitField()
    bf.data = b"\x80"
    bf[0] = True
    bf[-1] = False
    assert bf.data == b"\x01"


def test_bitfield_set_bit_index_with_int():
    """Set bit value by index using integer value."""
    bf = BitField()
    bf.data = b"\x80"
    bf[0] = 1
    bf[-1] = 0
    assert bf.data == b"\x01"


def test_bitfield_set_bit_index_with_invalid_type():
    """Set bit value by index using invalid integer value."""
    bf = BitField()
    with pytest.raises(TypeError):
        bf[0] = 2.0


def test_bitfield_invalid_bit_index():
    """Get/Set bit index with an invalid index value."""
    bf = BitField()
    with pytest.raises(IndexError):
        print(bf[8])
    with pytest.raises(IndexError):
        bf[8] = 1


def test_custom_bitfield_creation():
    """Create custom bitfield."""

    tbf = TestBitField()
    assert tbf.bit_length == 16
    assert len(tbf) == 2
    assert tbf.data == b"\x00\x00"
    assert tbf.flags == {"first_bit": False, "middle_bit": 0, "last_bit": False}


def test_bitfield_init_with_data():
    """Test BitField instantiation with data."""
    init_data = b"\xFF"
    bf = BitField(data=init_data)
    assert bf.data == init_data


def test_bitfield_str_dunder():
    """Test BitField __str__."""
    bf = BitField()
    assert str(bf) == r"BitField(00000000, flags={})"
    bf.data = b"\x01"
    assert str(bf) == r"BitField(10000000, flags={})"
    tbf = TestBitField()
    assert str(tbf) == r"TestBitField(0000000000000000, flags={'first_bit': False, 'middle_bit': 0, 'last_bit': False})"
    tbf.data = b"\x01\x02"
    assert str(tbf) == r"TestBitField(1000000001000000, flags={'first_bit': True, 'middle_bit': 2, 'last_bit': False})"


def test_bitfield_repr_dunder():
    """Test BitField __repr__."""
    bf = BitField()
    assert repr(bf) == "BitField(data=b'\\x00')"
    bf.data = b"\x01"
    assert repr(bf) == "BitField(data=b'\\x01')"


def test_custom_bitfield_invalid_byte_length():
    """Test exception of custom BitField with invalid `byte_length`."""
    with pytest.raises(ValueError):

        class BadBitField(BitField):
            """BadBitField Class."""

            byte_length = 0

        _ = BadBitField()


def test_get_named_bit_pos_on_non_bitfield():
    """Test exception when getting named bit from non-bitfield class."""
    with pytest.raises(TypeError):

        class BadClass:
            """Non-BitField Class."""

            named_bit = BitPos(0)

        bc = BadClass()
        _ = bc.named_bit


def test_bit_pos_invalid_bit_width():
    """Test exception of BitPos with invalid bit_width."""
    with pytest.raises(ValueError):

        class TestClass(BitField):
            """Test Class."""

            named_bit = BitPos(0, bit_width=0)

        _ = TestClass()


def test_set_named_bit_pos_on_non_bitfield():
    """Test exception when setting named bit from non-bitfield class."""
    with pytest.raises(TypeError):

        class BadClass:
            """Non-BitField Class."""

            named_bit = BitPos(0)

        bc = BadClass()
        bc.named_bit = True


def test_named_bit_get():
    """Get bitfield bit using named bit."""
    tbf = TestBitField()
    assert tbf.data == b"\x00\x00"
    assert tbf.first_bit is False
    tbf.data = b"\x01\x00"
    assert tbf.first_bit is True
    assert tbf.flags == {"first_bit": True, "middle_bit": 0, "last_bit": False}


def test_named_bit_set_with_bool():
    """Set bitfield bit using named bit and a boolean value."""
    tbf = TestBitField()
    assert tbf.data == b"\x00\x00"
    tbf.first_bit = True
    assert tbf.first_bit is True
    tbf.first_bit = False
    assert tbf.first_bit is False
    assert tbf.flags == {"first_bit": False, "middle_bit": 0, "last_bit": False}


def test_named_bit_set_with_valid_int():
    """Set bitfield bit using named bit and a valid integer value."""
    bf = TestBitField()
    assert bf.data == b"\x00\x00"
    bf.first_bit = 1
    assert bf.first_bit is True
    bf.first_bit = 0
    assert bf.first_bit is False


def test_bitfield_get_wide_bitpos():
    """Test get BitPos with non-standard bit width."""

    class CustomBitField(BitField):
        """Custom BitField with named multi-bit BitPos."""

        lower = BitPos(0, bit_width=4)
        upper = BitPos(4, bit_width=4)

    cbf = CustomBitField(data=b"\xF0")
    assert cbf.data == b"\xf0"
    assert bin(cbf.data[0]) == "0b11110000"
    assert cbf.lower == 0
    assert cbf.upper == 15
    assert cbf.flags == {"lower": 0, "upper": 15}

    cbf.data = b"\xa5"
    assert cbf.data == b"\xa5"
    assert bin(cbf.data[0]) == "0b10100101"
    assert cbf.lower == 5
    assert cbf.upper == 10
    assert cbf.flags == {"lower": 5, "upper": 10}


def test_bitfield_set_wide_bitpos():
    """Test set BitPos with non-standard bit width."""

    class CustomBitField(BitField):
        """Custom BitField with named multi-bit BitPos."""

        lower = BitPos(0, bit_width=4)
        upper = BitPos(4, bit_width=4)

    cbf = CustomBitField(data=b"\x00")
    assert cbf.data == b"\x00"
    assert bin(cbf.data[0]) == "0b0"
    cbf.upper = 10
    assert bin(cbf.data[0]) == "0b10100000"
    assert cbf.upper == 10
    assert cbf.lower == 0
    cbf.lower = 5
    assert bin(cbf.data[0]) == "0b10100101"
    assert cbf.upper == 10
    assert cbf.lower == 5
    cbf.upper = 16
    assert bin(cbf.data[0]) == "0b101"


def test_convert_bit_mask_to_bitpos():
    """Test converting bit mask integers into BitPos instances."""
    for bit_width in range(65):
        val = 0
        for _ in range(bit_width):
            val = (val << 1) | 1
        for idx in range(65 - bit_width):
            if bit_width == 0:
                with pytest.raises(ValueError):
                    bit_pos = mask2bitpos(val)
            else:
                bit_pos = mask2bitpos(val)
                assert bit_pos.bit_width == bit_width
                assert bit_pos.idx == idx
                val <<= 1


def test_convert_invalid_bit_mask_to_bitpos():
    """Test converting invalid bit mask integers into BitPos instances."""
    invalid_masks = [0b0, 0b101, 0b1101, 0b1011, 0b10000001]

    for mask in invalid_masks:
        with pytest.raises(ValueError):
            _ = mask2bitpos(mask)


def test_convert_bitpos_to_bit_mask():
    """Test converting BitPos instances bit mask integers."""
    assert bitpos2mask(BitPos(0)) == 0x1
    assert bitpos2mask(BitPos(1)) == 0x2
    assert bitpos2mask(BitPos(2)) == 0x4
    assert bitpos2mask(BitPos(3)) == 0x8
    for bit_width in range(65):
        val = 0
        for _ in range(bit_width):
            val = (val << 1) | 1
        for idx in range(65 - bit_width):
            if bit_width == 0:
                with pytest.raises(ValueError):
                    bit_pos = BitPos(idx, bit_width=bit_width)
            else:
                bit_pos = BitPos(idx, bit_width=bit_width)
                assert bitpos2mask(bit_pos) == val
            val <<= 1
