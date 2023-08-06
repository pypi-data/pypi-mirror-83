def get_from_path(obj, path, delim="."):
    splitted = path.split(delim)
    for k in splitted:
        if hasattr(obj, "get"):
            obj = obj.get(k)
        elif iterable(obj) and is_int(k):
            obj = obj[int(k)]
    return obj


def is_int(obj):
    if isinstance(obj, str):
        try:
            int(obj)
        except Exception:
            return False
        else:
            return True
    return isinstance(obj, int)


def iterable(obj):
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True


def urljoin(*pieces):
    return '/'.join(s.strip('/') for s in pieces)


def is_any_defined(*args):
    return any(args)


def is_all_defined(*args):
    return all(args)


def is_all_same_type(item_type, iterable):
    return all(isinstance(item, item_type) for item in iterable)
