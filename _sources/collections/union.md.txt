# Union

A Union is a dynamic byteclass created using the `@union` decorator.

```python
@union
class MyUnion:
    """My Union Byteclass."""

    var1: UInt64
    var2: UInt32
```

Similar to a C `union`, each member of a byteclass `union` has an offset of 0 and overlay onto the same underlying data.

The length of a Union byteclass is determined when the class is created based on its members.

A Union byteclass can contain both byteclass primitives and other byteclass collections.

Each Union member has its own `byte_order`. However, the `union` decorator accepts a `byte_order` parameter which is used for any members that rely on a `default_factory` for instantiation.

```python
@union(byte_order=b"@")
class Union1:
    """A union byteclass with one member using default factory."""

    a: UInt64 = member(default_factory=UInt64)

@union
class Union2:
    """A union byteclass with one member using default factory."""

    a: UInt64
```

The `Union1` and `Union2` defined above are functionally equivalent.
