import inspect


def select_values(obj, *keys):
    return [getattr(obj, k, None) for k in keys]



