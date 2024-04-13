"""Fixed collection factory."""

import keyword
import types
from collections.abc import ByteString, Iterable
from typing import Any

from ..._enums import ByteOrder
from .member import Member
from .structure import structure
from .union import union

__all__ = [
    "make_fixed_collection",
]


def make_fixed_collection(  # pylint: disable=R0912,R0913,R0914
    collection_type: str,
    cls_name: str,
    members_: Iterable[tuple[str, type]] | Iterable[tuple[str, type, Member]],
    *,
    bases=(),
    namespace: dict[str, Any] | None = None,
    byte_order: ByteString | ByteOrder = ByteOrder.NATIVE,
    packed: bool = False,
):
    """Return a new dynamically created fixed collection.

    The fixed collection name will be 'cls_name'.  'members' is an iterable
    of either (name, type) or (name, type, Member) objects.  Member objects are created
    by the equivalent of calling 'member(name, type [, Member-info])'.

    ```python
      C = make_fixed_collection('structure', 'C', [('x', Int8), ('y', Int32, member())],
      bases=(Base,))
    ```

    is equivalent to:

    ```python
      @structure
      class C(Base):
          x: Int8
          y: Int32 = member()
    ```

    For the bases and namespace parameters, see the builtin type() function.

    The parameters byte_order and packed are passed to the decorator based on the
    collection type. The packed parameter is only used for the structure type.
    """
    if namespace is None:
        namespace = {}

    # While we're looking through the field names, validate that they
    # are identifiers, are not keywords, and not duplicates.
    seen = set()
    annotations = {}
    defaults = {}
    for item in members_:
        if isinstance(item, tuple):
            if len(item) == 2:
                (
                    name,
                    item_type,
                ) = item  # type: ignore
            elif len(item) == 3:
                name, item_type, spec = item  # type: ignore
                defaults[name] = spec
            else:
                raise TypeError(f"Invalid member: {item!r}")
        else:
            raise TypeError(f"Invalid member: {item!r}")

        if not isinstance(name, str) or not name.isidentifier():
            raise TypeError(f"Field names must be valid identifiers: {name!r}")
        if keyword.iskeyword(name):
            raise TypeError(f"Field names must not be keywords: {name!r}")
        if name in seen:
            raise TypeError(f"Field name duplicated: {name!r}")

        seen.add(name)
        annotations[name] = item_type

    # Update 'ns' with the user-supplied namespace plus our calculated values.
    def exec_body_callback(namespace_):
        namespace_.update(namespace)
        namespace_.update(defaults)
        namespace_["__annotations__"] = annotations

    # We use `types.new_class()` instead of simply `type()` to allow dynamic creation
    # of generic dataclasses.
    cls = types.new_class(cls_name, bases, {}, exec_body_callback)

    # Convert byte_order to a ByteOrder object if needed.
    byte_order = ByteOrder(byte_order)

    # Apply the normal decorator.
    if collection_type == "structure":
        return structure(cls, byte_order=byte_order, packed=packed)
    if collection_type == "union":
        return union(cls, byte_order=byte_order)
    raise ValueError(f"Unknown collection type: {collection_type!r}")
