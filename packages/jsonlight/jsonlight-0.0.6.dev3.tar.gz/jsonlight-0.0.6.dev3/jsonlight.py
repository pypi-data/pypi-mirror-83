import json
from datetime import datetime


typemap = {
    datetime: (lambda v: v.isoformat(), lambda d: datetime.fromisoformat(d)),
}


def dump(obj, tmap=None):
    typemap = tmap if tmap is not None else globals()['typemap']

    if hasattr(obj, '__jsondump__'):
        obj = obj.__jsondump__()

    if isinstance(obj, dict):
        return {key: dump(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [dump(value) for value in obj]

    for cls in typemap:
        if isinstance(obj, cls):
            return typemap[cls][0](obj)

    if isinstance(obj, (str, float, int)):
        return obj

    return str(obj)


def dumps(obj, tmap=None):
    return json.dumps(dump(obj, tmap))


def load(cls, data, tmap=None):
    if hasattr(cls, '__jsonload__'):
        return cls.__jsonload__(data)
    typemap = tmap if tmap is not None else globals()['typemap']
    if cls in typemap:
        return typemap[cls][1](data)
    return cls(data)


def loads(cls, data, tmap=None):
    data = json.loads(data)
    return load(cls, data, tmap)
