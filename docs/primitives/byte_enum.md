# ByteEnum Primitive

A `ByteEnum` is an adapter class that allows you to map an `IntEnum` class to a `byteclass` integer class such as `UInt8`.

A `ByteEnum` will derive it's behavior from the assigned integer class, but use the `IntEnum` class for representation.

The `byte_length` of a `ByteEnum` instance is dependent on the `byteclass` integer class.
