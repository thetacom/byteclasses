# FixedArray

Fixed size arrays provide a concrete class that accepts an instance of a byteclass and a qty during instantiation.

> `FixedArray` has a minimum qty of two.

```python
fa1 = FixedArray(2) # Item type for FixedArrays are UInt8
fa2 = FixedArray(2, Int16)
fa3 = FixedArray(4, Int16, byte_order=b"!")
```

> The `FixedArray` `byte_order` will override the item `byte_order` regardless if the item `byte_order` is specified.

`FixedArray` can only contain byteclass primitives, they do not accept collections as their item.

Array items can be accessed by indexing an array. The raw array bytes can be interacted with via the `data` attribute.

```python
fa = FixedArray(10, Int8)
print(fa)
print(fa.data)
print(fa[0])
print(fa[0].data)
```

Assignment while indexing a FixedArray will assign the provided value the the `data` attribute of the specified item index.
