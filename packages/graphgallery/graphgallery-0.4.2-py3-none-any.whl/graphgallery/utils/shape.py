import itertools
from numbers import Number
from graphgallery.utils.type_check import is_iterable

def repeat(src, length):
    if src is None:
        return [None for _ in range(length)]
    if src == [] or src == ():
        return []
    if isinstance(src, (Number, str)):
        return list(itertools.repeat(src, length))
    if (len(src) > length):
        return src[:length]
    if (len(src) < length):
        return list(src) + list(itertools.repeat(src[-1], length - len(src)))
    return src


def get_length(obj):
    if is_iterable(obj):
        length = len(obj)
    else:
        length = 1
    return length
