# String

`String` provides a concrete class array of UChar primitives that accepts a length during instantiation.

Optional parameter also include `value` and `data`. These parameters are mutually exclusive.

All strings are null terminated by default and this property is internally enforced. To disable null_termination, set `null_terminated` to `False` during instantiation.

```python
string1 = String(8)
string2 = String(8, value="initial")
string3 = String(8, data=b"initial\x00")
string4 = String(8, data=b"initials", null_terminated=False)
```
