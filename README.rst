===========
Strict hint
===========

**Strict hint** provides a way to do runtime type checks based based on type hint annotations introduced by PEP-484_.


Usage is quite simple, just add type annotations to a function or method and decorate it with `@strict`:

.. code-block:: python

    from strict_hint import strict

    @strict
    def add(a: int: b: int) -> int:
        return a+b

If non `int` will be passed, a `TypeError` will be raised.
Same will happen if function would return different type than expected.

Type checks support (for arguments and returned values):
 - all primitive type hints: `int`, `float`, `list`, `tuple`, `set`, `dict`, etc.,
 - standard interpreter types eg.: `FunctionType` and other,
 - tuples of types, eg: `(int, float)` will allow for both types to be accepted,
 - default values, also of different type than annotation: eg. `a: int = None`
 - used defined classes and class inheritance
 
 .. _PEP-484: https://www.python.org/dev/peps/pep-0484/
