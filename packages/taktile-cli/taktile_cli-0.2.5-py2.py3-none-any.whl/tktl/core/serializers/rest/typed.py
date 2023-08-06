from collections.abc import Sequence
from functools import singledispatch
from typing import Dict, List, Optional, Type, Union

import numpy
import pandas
from pandas.core.dtypes.inference import is_sequence
from pydantic import create_model

from tktl.core.serializers.base import CustomDeserializingModelT
from tktl.core.serializers.rest.schema import (
    get_array_model,
    get_dataframe_model,
    get_mapping_model,
    get_nested_sequence_model,
    get_series_model,
    get_single_value_model,
)
from tktl.core.t import RestSchemaTypes


@singledispatch
def to_pydantic(
    value, name: str = "SingleValue"
) -> Type[CustomDeserializingModelT]:  # noqa
    single_value_model = get_single_value_model(value)
    single_value_model.__name__ = name
    return single_value_model


@to_pydantic.register
def _(
    value: pandas.DataFrame, name: str = RestSchemaTypes.DATAFRAME.value, nullable=True
):
    """Create a Pydantic model for a batch from a Pandas DataFrame

    Parameters
    ----------
    value : pd.DataFrame
        Input Dataframe
    name : str, optional
        Name for the model, by default "DataFrame"
    nullable : bool, optional
        Indicates whether observations can be missing (None), by default True

    Returns
    -------
    ModelMetaclass
        Pydantic model of the dataframe
    """
    type_map = {}
    example_map = {}

    for col, values in value.to_dict().items():
        types = (type(v) for k, v in values.items() if v is not None)
        var_type = next(types, str)  # type of first item that is not None
        if nullable:
            var_type = Optional[var_type]
        nxt_val = next(v for k, v in values.items() if v is not None)
        type_map[col] = (var_type, None)
        example_map[col] = nxt_val

    index_type = type(next((t for t in value.index)))
    type_map["index"] = (index_type, None)

    DynamicBaseModel = create_model(name, **type_map)  # noqa
    DynamicBaseModel.__name__ = name
    return get_dataframe_model(base_model=DynamicBaseModel, example=[example_map])


@to_pydantic.register
def _(value: pandas.Series, name: str = RestSchemaTypes.SERIES.value):
    """Create a Pydantic model for a batch from a Pandas Series

    Parameters
    ----------
    value : pd.Series
        Input Dataframe
    name : str, optional
        Name for the model, by default "DataFrame"
    nullable : bool, optional
        Indicates whether observations can be missing (None), by default True

    Returns
    -------
    ModelMetaclass
        Pydantic model of the series
    """
    nullable = True if value.isna().sum() > 0 else False
    type_name = "Outcome" if not value.name else value.name
    type_map = {}
    types = (type(v) for k, v in value.to_dict().items() if v is not None)
    var_type = next(types, str)  # type of first item that is not None
    if var_type == bool:
        var_type = Union[var_type, float]
    if nullable:
        var_type = Optional[var_type]
    type_map[type_name] = (List[var_type], None)
    DynamicBaseModel = create_model(name, **type_map)  # noqa
    DynamicBaseModel.__name__ = name
    return get_series_model(series=value, base_model=DynamicBaseModel)


@to_pydantic.register
def _(value: numpy.ndarray, name: str = RestSchemaTypes.ARRAY.value):
    """Create a Pydantic model for a batch from a Pandas Series

    Parameters
    ----------
    value : numpy.ndarray
    name : str, optional
        Name for the model, by default "DataFrame"

    Returns
    -------
    ModelMetaclass
        Pydantic model of the series
    """
    as_list = value.tolist()
    if len(value.shape) == 1:
        return List[type(as_list[0])]
    else:
        list_model = get_nested_sequence_model(as_list)
        array_model = get_array_model(list_model)
        array_model.__name__ = name
    return array_model


@to_pydantic.register
def _(value: Sequence, name: str = RestSchemaTypes.SEQUENCE.value):
    """Create a Pydantic model for a batch from a Pandas Series

    Parameters
    ----------
    value : Union[List, Dict]
        Input values, either Dict or List
    name : str, optional
        Name for the model, by default "DataFrame"

    Returns
    -------
    ModelMetaclass
        Pydantic model of the series
    """

    if isinstance(value, list) or isinstance(value, tuple):
        if len(value) > 0:
            first = value[0]
            if isinstance(first, list):
                sequence_model = get_nested_sequence_model(first)
                sequence_model.__name__ = name

            elif isinstance(first, dict):
                mapping_model = _dict_model(
                    value=first, name=RestSchemaTypes.DICT.value
                )
                sequence_model = get_mapping_model(base_model=mapping_model)
            # more specific than numpy's is_sequence implementation
            elif not is_sequence(first):
                sequence_model = get_single_value_model(first)
                sequence_model.__name__ = name
            else:
                raise
        else:
            raise ValueError("Input must be non-empty")
    else:
        raise
    return sequence_model


@to_pydantic.register
def _(value: dict, name: str = RestSchemaTypes.DICT.value):
    mapping_model = _dict_model(value=value, name=name)
    mapping_model.__name__ = name
    return mapping_model


def _dict_model(value, name):
    types = {k: (type(v), v) for k, v in value.items()}
    return create_model(name, **types)


def _get_df_example(example_map):
    class Config:
        schema_extra = {"example": example_map}

    return Config
