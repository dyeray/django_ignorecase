def safe_traverse(obj, *args):
    for item in args:
        obj = getattr(obj, item, None)
        if obj is None:
            break
    return obj
