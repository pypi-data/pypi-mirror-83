import collections
from typing import (
    Dict,
    List,
    Tuple,
)


def is_not_none(v):
    return v is not None


def is_essential(v):
    return bool(v)


def filter_none(l, predicate=is_not_none):
    if isinstance(l, dict):
        return {k: v for k, v in l.items() if predicate(v)}
    elif isinstance(l, collections.Iterable):
        return list(filter(lambda x: x is not None, l))
    else:
        return l


def is_iterable(i):
    try:
        iter(i)
    except TypeError:
        return False
    else:
        return True


def noneless(d, predicate=is_not_none):
    if isinstance(d, Dict):
        return {i: noneless(v) for i, v in d.items() if predicate(v)}
    elif isinstance(d, (Tuple, List)):
        return list(map(noneless, d))
    else:
        return d


def paginator(func, page_size, *args, **kwargs):
    page = 1
    while True:
        data = func(page=page, page_size=page_size, *args, **kwargs)
        yield data
        if data.total < data.page * data.page_size:
            return
        page += 1


def flatten(d, sep='.', prefix=''):
    items = []
    for k, v in d.items():
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, sep=sep, prefix=prefix + k + sep).items())
        else:
            items.append((prefix + k, v))
    return dict(items)


def unflatten(flat_dict, sep='.'):
    unflatted_dict = {}
    for key, value in flat_dict.iteritems():
        parts = key.split(sep)
        d = unflatted_dict
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
    return unflatted_dict


def merge_dicts(d1, *args):
    merged = dict(d1)
    for d in args:
        merged.update(d)
    return merged


def next_greater_power_of_2(x):
    return 2 ** (x - 1).bit_length()


def smart_merge_dicts(destination, source, list_policy='merge', copy=True):
    if copy:
        destination = dict(destination)

    for key, value in source.items():
        if isinstance(value, dict):
            policy = value.pop('_policy', 'merge')
            if policy == 'override':
                destination[key] = value
            elif policy == 'bypass':
                if key not in destination:
                    destination[key] = value
            elif policy == 'merge':
                destination.setdefault(key, {})
                destination[key] = smart_merge_dicts(destination[key], value, list_policy=list_policy)
        elif isinstance(value, (tuple, list)) and list_policy == 'merge':
            destination.setdefault(key, [])
            if isinstance(destination[key], (tuple, list)):
                destination[key] = [_ for _ in destination[key]]
                destination[key].extend(value)
            else:
                destination[key] = value
        else:
            destination[key] = value

    return destination


class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result
