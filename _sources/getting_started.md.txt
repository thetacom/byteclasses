# Getting Started

Manipulating raw byte can often be cumbersome and tedious. This package is intended
 to make handling, parsing, and interpreting raw data a simpler and more inuititive endeavor.

The components provided by this package can be grouped into two basic categories, `primitives` and `collections`.

## `primitives`

Primitive Types - The primitive types provide the base level elements used to compose larger and more complex data structures.

* `integers` - All integer primitives have a fixed length with a configurable `byte_order`.
  * `Int8`, `UInt8`, `Int16`, `UInt16`, `Int32`, `Long`, `ULong`, `Int64`, `UInt64`
  * Aliases: `SChar`, `UChar`, `Byte`, `Short`, `UShort`, `Word`, `Int`, `UInt`, `DWord`, `LongLong`, `ULongLong`
  * Special: `Bit`
* `floats` - All float primitives have a fixed length with a configurable `byte_order`.
  * `Float16`, `Float32`, `Float64`
  * Aliases: `Half`, `Float`, `Double`
* `bitfield` - A generic primitive for easily extracting bit values from a byte. Fixed length is one (1) byte by default. Can be subclassed for multibyte bitfields.
  * `BitField`

## `collections`

Collection Types - Collection types allow you to combine primitives or other collections based on their specified behavior.

* `FixedArray` - A concrete fixed size collection class containing a single primitive type or specified quantity.
* `Union` - A dynamic byteclass implemented via the `@union` decorator. Behaves similar to a C `union`.
* `Structure` - A dynamic byteclass implemented via the `@structure` decorator. Behaves similar to a C `struct`.

## Attaching external data

Byteclasses can be attached to any bytes like external data.
Use the byteclass `.attach(mv)` method to connect a `memoryview` of the external data to the internal data attribute of the byteclass instance.
> The length of the `memoryview` must match the length of the item it is being attached to.
