# Getting Started

Manipulating raw byte can often be cumbersome and tedious. This package is intended
 to make handling, parsing, and interpreting raw data a simpler and more inuititive endeavor.

The components provided by this package can be grouped into two basic categories, `primitives` and `collections`.

## `primitives`

Primitive Types - The primitive types provide the base level elements used to compose larger and more complex data structures.

* `generics` - Generic fixed length types.
  * `Byte`, `Word`, `DWord`, `QWord`
* `bitfield` - A generic primitive for easily extracting bit values from a byte. Fixed length is one (1) byte by default. Can be subclassed for multibyte bitfields.
  * `BitField`, `BitPos`
* `integers` - All integer primitives have a fixed length with a configurable `byte_order`.
  * `Int8`, `UInt8`, `Int16` (`Short`), `UInt16` (`UShort`), `Int32` (`Int`), `UInt32` (`UInt`), `Long`, `ULong`, `Int64` (`LongLong`), `UInt64` (`ULongLong`)
* `floats` - All float primitives have a fixed length with a configurable `byte_order`.
  * `Float16` (`Half`), `Float32` (`Float`), `Float64` (`Double`)
* `characters` - Single byte character classes.
  * `UChar` (`Char`), `SChar`

## `collections`

Collection Types - Collection types allow you to combine primitives or other collections based on their specified behavior.

* `FixedArray` - A concrete fixed size collection class containing a single primitive type or specified quantity.
* `String` - A specialized subclass of FixedArray to add string convenience methods.
* `Structure` - A dynamic byteclass implemented via the `@structure` decorator. Behaves similar to a C `struct`.
* `Union` - A dynamic byteclass implemented via the `@union` decorator. Behaves similar to a C `union`.

## Attaching external data

Byteclasses can be attached to any bytes like external data.
Use the byteclass `.attach(data)` method to connect a `memoryview` of the external data to the internal data attribute of the byteclass instance.
> The length of the `memoryview` must match the length of the item it is being attached to.

> If a `bytes` or `bytearray` object is passed to `attach`, a `bytearray` `memoryview` will be created. If you intend for byteclasses to all interact with a single data instance, create a `memoryview` of your data and pass to appropriate slice of the `memoryview` to `attach`.
