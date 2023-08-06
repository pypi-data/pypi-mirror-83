jsonlight: json with rudimentary type encoding/decoding for Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds support for a couple of new Python magic methods to make Python object
oriented JSON encoding and decoding a bit easier, with the following goals in
mind:

- jsonlight.dumps should always work, even if it has to fallback to a string
- it detects if an object being dumped defines a ``__jsondump__`` method
- it detects if an object being dumped is of a type defined in the global
  typemap, or the one that's being used
- for complete round-tripping, the type schema is maintained in a
  ``__jsonload__`` method that you must implement

Standard types
--------------

This is what you can already do in Python:

.. code:: python

    from json import loads, dumps
    from uuid import UUID, uuid4

    obj = uuid4()
    assert obj == UUID(loads(dumps(str(obj))))

All standard Python types such as UUID must have an encode/decode method in the
default typemap provided by jsonlight, so encoding to JSON should always work.
However, the type must be specified on load:

.. code:: python

    from jsonlight import loads, dumps
    from uuid import UUID, uuid4

    obj = uuid4()
    assert obj == loads(UUID, dumps(obj))

You can see that the main difference with ``json.loads`` is that
``jsonlight.loads`` requires a type as first argument. This is because
``jsonlight.loads`` will first call ``json.loads`` to convert the string into a
Python object with basic JSON tyes, and then pass that to the type's
``__jsonload__`` function, or rely on the typemap defined functions if any.

Nested types
------------

You may leverage the ``__jsondump__`` and ``__jsonload__`` methods based on the
following conventions:

- ``__jsondump__``: return a representation of self with JSON data types
- ``__jsonload__``: instanciate an object based on the result from __jsondump__

Example:

.. code-block:: python

    from jsonlight import load

    class YourClass:
        def __init__(self):
            self.now = datetime.now()

        def __jsondump__(self):
            return dict(now=self.now)

        @classmethod
        def __jsonload__(cls, data):
            return cls(load(datetime, data['now'])


As you can see:

- you don't have to worry about calling ``__jsondump__`` on return values of
  your own ``__jsondump__`` because ``jsonlight.dumps`` will do that
  recursively,
- you have full control on deserialization just like with ``__setstate__``, but
  if you call jsonlight.load in there yourself then you don't have to
  duplicate deserialization logic on nested objects,

Typemaps
--------

This lib must support all standard Python types, and it already works for
things like UUID or Path because they cast fine from and to strings. However,
this is not the case for datetimes and there is no JSON standard for datetimes.

Since it is a requirement for jsonlight to support all standard python types, a
default typemap is also included, which makes datetimes export to string with
``.isoformat()`` and from string with ``.fromisoformat()``:

.. code-block:: python

    now = datetime.now()
    assert now == loads(datetime, dumps(now))

This is the reason why we have typemaps. The typemap in jsonlight maps a Python
type to a couple of encoding/decoding functions, so that we have something that
works without monkey patching.

To illustrate how to use a specific typemap, let's decide we want to remove the
leading slash of all Path objects dumps and ensure there is one on load, we
will define our own typemap:

.. code-block:: python

    typemap = {
        Path: (
            lambda value: str(value).lstrip('/'),
            lambda data: Path('/' + data.lstrip('/')),
        ),
    }
    assert dumps(Path('/foo/bar'), typemap) == '"foo/bar"'
    assert loads(Path, '"foo/bar"', typemap) == Path('/foo/bar')

A couple of possibilities are left to keep in mind:

- ``typemap.update(jsonlight.typemap)`` adds the default jsonlight typemap to
  your own,
- ``jsonlight.typemap.update(typemap)`` adds your own typemap on top of the
  default typemap.
