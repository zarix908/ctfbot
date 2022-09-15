def deep_get(obj, key):
    path = key.split('.')
    current = obj

    for k in path:
        if current is None:
            return None
        current = array_or_dict_get(current, k)

    return current


def array_or_dict_get(obj, key):
    try:
        return obj[int(key)]
    except (ValueError, IndexError):
        return obj.get(key)
