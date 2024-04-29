# ByteArray

Fixed size arrays provide a concrete class that accepts an instance of a byteclass and a qty during instantiation.

> `ByteArray` has a minimum qty of two.

```python
fa1 = ByteArray(2) # Item type for ByteArrays are UInt8
fa2 = ByteArray(2, Int16)
fa3 = ByteArray(4, Int16, byte_order=b"!")
```

> The `ByteArray` `byte_order` will override the item `byte_order` regardless if the item `byte_order` is specified.

`ByteArray` can only contain byteclass primitives, they do not accept collections as their item.

Array items can be accessed by indexing an array. The raw array bytes can be interacted with via the `data` attribute.

```python
fa = ByteArray(10, Int8)
print(fa)
print(fa.data)
print(fa[0])
print(fa[0].data)
```

Assignment while indexing a ByteArray will assign the provided value the the `data` attribute of the specified item index.
