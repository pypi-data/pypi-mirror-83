"""Inspired by Keras backend config API. https://tensorflow.google.com """

from tensorflow.keras import backend as K
from typing import Union

from graphgallery.backend import TensorFlowBackend, PyTorchBackend

# used to store the model or weights for tf and torch
POSTFIX  = ".h5"

_BACKEND = TensorFlowBackend()
_MODULE_KIND = {"tf": "T", "tensorflow": "T", "T": "T",
                "th": "P", "torch": "P", "pytorch": "P", "P": "P"}

_ALLOWED_NAME = set(list(_MODULE_KIND.keys()))

_MODULE = {"T": TensorFlowBackend,
           "P": PyTorchBackend}

_INT_TYPES = {'int16', 'int32', 'int64'}
_FLOAT_TYPES = {'float16', 'float32', 'float64'}

# The type of integer to use throughout a session.
_INTX = 'int32'
# The type of float to use throughout a session.
_FLOATX = 'float32'

epsilon = K.epsilon
set_epsilon = K.set_epsilon


def floatx() -> str:
    """Returns the default float type, as a string.

    E.g. `'float16'`, `'float32'`, `'float64'`.

    Returns:
    --------
    String, the current default float type.

    Example:
    --------
    >>> graphgallery.floatx()
    'float32'
    """
    return _FLOATX


def set_floatx(dtype: str) -> str:
    """Sets the default float type.

    Parameters:
    --------
    dtype: String; `'float16'`, `'float32'`, or `'float64'`.

    Example:
    --------
    >>> graphgallery.floatx()
    'float32'
    >>> graphgallery.set_floatx('float64')
    'float64'

    Raises:
    --------
    ValueError: In case of invalid value.
    """

    if dtype not in _FLOAT_TYPES:
        raise ValueError(f"Unknown floatx type: '{str(dtype)}', expected one of {_FLOAT_TYPES}.")
    global _FLOATX
    _FLOATX = str(dtype)
    return _FLOATX


def intx() -> str:
    """Returns the default integer type, as a string.

    E.g. `'int16'`, `'int32'`, `'int64'`.

    Returns:
    --------
    String, the current default integer type.

    Example:
    --------
    >>> graphgallery.intx()
    'int32'

    Note:
    -------
    The default integer type of PyTorch backend will set to
        'int64', i.e., 'Long'.
    """
    return _INTX


def set_intx(dtype: str) -> str:
    """Sets the default integer type.

    Parameters:
    --------
    dtype: String; `'int16'`, `'int32'`, or `'int64'`.

    Example:
    --------
    >>> graphgallery.intx()
    'int32'
    >>> graphgallery.set_intx('int64')
    'int64'

    Raises:
    --------
    ValueError: In case of invalid value.
    RuntimeError: PyTorch backend using other integer types.
    """

    if dtype not in _INT_TYPES:
        raise ValueError(f"Unknown floatx type: '{str(dtype)}', expected one of {_INT_TYPES}.")
    global _INTX

    if _BACKEND.kind == "P" and dtype != 'int64':
        raise RuntimeError(
            f"For {_BACKEND}, tensors used as integer must be long (int64), not '{str(dtype)}'.")

    _INTX = str(dtype)
    return _INTX


def backend() -> Union[TensorFlowBackend, PyTorchBackend]:
    """Publicly accessible method
    for determining the current backend.

    Returns
    --------
    String, the backend that GraphGallery is currently using.

    E.g. `'TensorFlow 2.1.2 Backend'`,
      `'PyTorch 1.6.0+cpu Backend'`.

    Returns:
    --------
    String, the current default backend module.

    Example:
    --------
    >>> graphgallery.backend()
    'TensorFlow 2.1.2 Backend'
    """
    return _BACKEND


def set_backend(module_name: str) -> Union[TensorFlowBackend, PyTorchBackend]:
    """Sets the default backend module.

    Parameters:
    --------
    module_name: String; `'tf'`, `'tensorflow'`,
             `'th'`, `'torch'`, 'pytorch'`.

    Example:
    --------
    >>> graphgallery.backend()
    'TensorFlow 2.1.2 Backend'
    
    >>> graphgallery.set_backend('torch')
    'PyTorch 1.6.0+cpu Backend'

    Raises:
    --------
    ValueError: In case of invalid value.
    """
    if module_name not in _ALLOWED_NAME:
        raise ValueError(
            f"Unknown module name: '{str(module_name)}', expected one of {_ALLOWED_NAME}.")
    global _BACKEND
    kind = _MODULE_KIND.get(module_name)
    if kind != _BACKEND.kind:
        # TODO: improve
        _BACKEND = _MODULE.get(kind)()

        if kind == "P":
            # PyTorch backend uses Long integer as default.
            set_intx('int64')
        else:
            # Using int32 is more efficient
            set_intx('int32')

    return _BACKEND
