# Byteclasses Python Package

[![Version](https://img.shields.io/pypi/v/byteclasses.svg)](https://pypi.python.org/pypi/byteclasses)
[![Status](https://img.shields.io/pypi/status/byteclasses)](https://pypi.python.org/pypi/byteclasses)
[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/byteclasses)](https://libraries.io/pypi/byteclasses)
[![Wheel](https://img.shields.io/pypi/wheel/byteclasses)](https://pypi.org/project/byteclasses/)
[![Downloads](https://img.shields.io/pypi/dm/byteclasses)](https://pypi.python.org/pypi/byteclasses)
[![License](https://img.shields.io/pypi/l/byteclasses.svg)](https://pypi.python.org/pypi/byteclasses)
[![Python Implementation](https://img.shields.io/pypi/implementation/byteclasses)](https://pypi.org/project/byteclasses/)
[![Python Version](https://img.shields.io/pypi/pyversions/byteclasses)](https://pypi.org/project/byteclasses/)

[![Lint](https://github.com/thetacom/byteclasses/actions/workflows/lint.yml/badge.svg)](https://github.com/thetacom/byteclasses/actions/)
[![Test](https://github.com/thetacom/byteclasses/actions/workflows/test.yml/badge.svg)](https://github.com/thetacom/byteclasses/actions/)
[![Release](https://github.com/thetacom/byteclasses/actions/workflows/release.yml/badge.svg)](https://github.com/thetacom/byteclasses/actions/)
[![Publish](https://github.com/thetacom/byteclasses/actions/workflows/publish.yml/badge.svg)](https://github.com/thetacom/byteclasses/actions/)

[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

![Logo](docs/imgs/byteclasses.png)

A python package designed to ease data manipulation tasks and improve efficiency when handling binary data.

## Installation

```console
> pip install byteclasses
```

## Description

Byteclasses provides a variety of convenience wrapper classes to simplify data handling. These wrapper classes automatically pack and unpack data values.

Additionally, certains types, such as byteclass integers, impose type specific constraints. For example, assigning the value 256 to a `UInt8` will raise an `OverflowError` exception.

This library contains a variety of fixed size primitive byteclasses. These primitive classes can be used in conjunction with the byteclass collections to build more complicated data elements.

Similiar to a Python `dataclass`, byteclass collections are constructured using the `structure` or `union` class decorators.
Whereas dataclasses have fields, byteclass collections have members. Collection members must be a byteclass type and cannot have a default value unless using the `member` constructor function. Each member will be instantiated using its type hint as a factory.

A byteclass structure and union behaves similar to a C struct and union respectively.

The `ByteArray` and `String` collections can be instantiated directly using the provided classes.

## Byteclasses

- Primitives
  - Generic - `BitField`, `Byte`, `Word`,`DWord`, `QWord`
  - Characters - `UChar` (`Char`), `SChar`
  - Floats - `Float16` (`Half`), `Float32` (`Float`),`Float64` (`Double`)
  - Integers - `Int8`, `UInt8`, `Int16` (`Short`), `UInt16` (`UShort`), `Int32` (`Int`), `UInt32` (`UInt`), `Long`, `ULong`, `Int64` (`LongLong`), `UInt64` (`ULongLong`)
  - Special - `ByteEnum`

- Collections
  - `ByteArray` - Class
  - `String` - Class
  - `structure` - Class Decorator
  - `union` - Class Decorator

## Simple Byteclass Structure Example

```python
from byteclasses.types.collections import structure
from byteclasses.types.primitives.integer import UInt8, UInt32

@structure
class MyStruct:
  """My custom byteclass structure."""

  member1: UInt8
  member2: UInt32

my_var = MyStruct()
```

## Docs

[Byteclasses Documentation](https://io.thetacom.info/byteclasses/)

## References

[C data types](https://en.wikipedia.org/wiki/C_data_types)
