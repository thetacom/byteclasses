# Byteclasses Package

## Description

A python package designed for creating and managing blobs of binary data using dataclass like classes.

This library is designed for creating custom Python data classes with builtin structural constraints. Byte Classes behave similar to a combination of Python dataclasses and C structs.

## Byte Classes

- Collections
- Primitives
  - Floats
  - Integers (FixedInt Metaclass)
    - Int8
      - Aliases: SChar
    - UInt8
      - Aliases: UChar, Byte
    - Bit
    - Int16
      - Aliases: Short
    - UInt16
      - Aliases: UShort, Word
    - Int32
      - Aliases: Int
    - UInt32
      - Aliases: UInt, DWord
    - Long
    - ULong
    - Int64
      - Aliases: LongLong
    - UInt64
      - Aliases: ULongLong
