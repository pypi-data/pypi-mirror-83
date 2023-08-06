import torch
import numpy as np
import tensorflow as tf
import scipy.sparse as sp

from abc import ABC
from typing import Any

from graphgallery import floatx, intx, backend
from graphgallery import (is_list_like,
                          is_interger_scalar,
                          is_tensor)



class Transform(ABC):

    def __init__(self):
        ...

    def __call__(self):
        ...


class NullTransform(Transform):
    def __init__(self, *args, **kwargs):
        ...

    def __call__(self, inputs: Any):
        return inputs

    def __repr__(self):
        return "NullTransform()"

    
def asintarr(x, dtype: str = None):
    """Convert `x` to interger Numpy array.

    Parameters:
    ----------
    x: Tensor, Scipy sparse matrix,
        Numpy array-like, etc.

    Returns:
    ----------
    Integer Numpy array with dtype or `graphgallery.intx()`

    """
    if dtype is None:
        dtype = intx()

    if is_tensor(x):
        if x.dtype != dtype:
            kind = backend().kind
            if kind == "T":
                x = tf.cast(x, dtype=dtype)
            else:
                x = x.to(getattr(torch, dtype))
        return x

    if is_interger_scalar(x):
        x = np.asarray([x], dtype=dtype)
    elif is_list_like(x) or isinstance(x, (np.ndarray, np.matrix)):
        x = np.asarray(x, dtype=dtype)
    else:
        raise ValueError(
            f"Invalid input which should be either array-like or integer scalar, but got {type(x)}.")
    return x


def indices2mask(indices, shape):
    mask = np.zeros(shape, np.bool)
    mask[indices] = True
    return mask
