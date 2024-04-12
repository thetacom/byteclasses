# Structure

A Structure is a dynamic byteclass created using the `@structure` decorator.

```python
@structure
class MyStructure:
    """My Structure Byteclass."""

    var1: UInt64 = UInt64()
    var2: UInt32 = UInt32()
```

Similar to a C `struct`, each member of a byteclass `structure` has a sequential offset. By default, `structure` are padded so each member is size aligned. The `structure` decorator accepts a boolean `padding` parameter to override the default padding behavior.

The length of a Structure byteclass is determined when the class is created based on its members.

A Structure byteclass can contain both byteclass primitives and other byteclass collections.

Each Structure member has its own `byte_order`. However, the `structure` decorator accepts a `byte_order` parameter which is used for any members that rely on a `default_factory` for instantiation.

```python
@structure(byte_order=b">")
class FactoryStructure:
    """A structure byteclass with member using default factory."""

    a: UInt64 = member(default_factory=UInt64)
```
