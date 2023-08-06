DICT = '__dict__'
SLOTS = '__slots__'


def keys(ob):
    return list(ob.keys()) if isinstance(ob, dict) \
        else list(ob.__dict__.keys()) if hasattr(ob, DICT) \
        else ob.__slots__ if hasattr(ob, SLOTS) \
        else []


def values(ob):
    return list(ob.values()) if isinstance(ob, dict) \
        else list(ob.__dict__.values()) if hasattr(ob, DICT) \
        else [getattr(ob, s) for s in ob.__slots__] if hasattr(ob, SLOTS) \
        else []


def entries(ob):
    return list(ob.items()) if isinstance(ob, dict) \
        else list(ob.__dict__.items()) if hasattr(ob, DICT) \
        else [(s, getattr(ob, s)) for s in ob.__slots__] if hasattr(ob, SLOTS) \
        else []


def to_dict(ob):
    return ob if isinstance(ob, dict) \
        else ob.__dict__ if hasattr(ob, DICT) \
        else {s: getattr(ob, s) for s in ob.__slots__} if hasattr(ob, SLOTS) \
        else {}
