""" Diffusion data types. """

from __future__ import annotations

import sys
from inspect import isclass
from typing import cast, Mapping, Optional, Type, Union

from diffusion.internal.utils import get_all_subclasses
from . import complex, simple
from .abstract import DataType
from .exceptions import (
    DataTypeError,
    IncompatibleDatatypeError,
    InvalidDataError,
    UnknownDataTypeError,
)

DataTypeArgument = Union[int, str, Type[DataType]]

_dt_module = sys.modules[__name__]  # this module

# set the data types as module attributes
for data_type in get_all_subclasses(DataType):
    if hasattr(data_type, "type_name"):
        setattr(_dt_module, data_type.type_name.upper(), data_type)

# index the implemented data types by type codes and cache them
_indexed_data_types: Mapping[int, Type[DataType]] = {
    item.type_code: item
    for item in vars(_dt_module).values()
    if isclass(item) and issubclass(item, DataType) and item is not DataType
}


def get(data_type: Optional[DataTypeArgument]) -> Type[DataType]:
    """ Helper function to retrieve a datatype based on its name or a `DataTypes` value.

    Args:
        data_type: Either a string that corresponds to the `type_name` attribute
                   of a `DataType` subclass, or an integer that corresponds to the
                   `type_code` of a `DataType` subclass. It also accepts an actual
                   `DataType` subclass, which is returned unchanged.

    Raises:
        `UnknownDataTypeError`: If the corresponding data type was not found.

    Examples:
        >>> get('string')
        <class 'diffusion.datatypes.simple.StringDataType'>
        >>> get(_dt_module.INT64)
        <class 'diffusion.datatypes.simple.Int64DataType'>
        >>> get(15)
        <class 'diffusion.datatypes.complex.JsonDataType'>
    """
    if isinstance(data_type, str):
        data_type = getattr(_dt_module, data_type.strip().upper(), None)
    if isinstance(data_type, int):
        data_type = _indexed_data_types.get(data_type)
    if isclass(data_type) and issubclass(data_type, DataType):  # type: ignore
        return cast(Type[DataType], data_type)
    raise UnknownDataTypeError(f"Unknown data type '{data_type}'.")
