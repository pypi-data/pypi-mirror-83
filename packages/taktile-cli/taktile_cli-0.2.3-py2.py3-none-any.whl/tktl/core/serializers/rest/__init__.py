from typing import Any, Dict, List, Sequence, Type, Union

import pandas
from pydantic import BaseModel

from tktl.core.serializers.base import CustomDeserializingModelT, ObjectSerializer
from tktl.core.t import RestSchemaTypes


class DataFrameSerializer(ObjectSerializer):
    @classmethod
    def deserialize(cls, value: CustomDeserializingModelT) -> pandas.DataFrame:
        return value.deserialize()

    @classmethod
    def serialize(
        cls, value: pandas.DataFrame, output_model: Type[BaseModel] = None
    ) -> BaseModel:
        return output_model.parse_obj(value.to_dict("records"))


class SeriesSerializer(ObjectSerializer):
    @classmethod
    def deserialize(cls, value: CustomDeserializingModelT) -> pandas.DataFrame:
        return value.deserialize()

    @classmethod
    def serialize(
        cls, value: pandas.Series, output_model: Type[BaseModel] = None
    ) -> BaseModel:
        name = _get_prop_from_series_schema(output_model)
        return output_model(**{name: value.tolist()})


class ArraySerializer(ObjectSerializer):
    @classmethod
    def deserialize(cls, value: CustomDeserializingModelT) -> pandas.DataFrame:
        return value.deserialize()

    @classmethod
    def serialize(cls, value: Any, output_model: Type[BaseModel] = None) -> BaseModel:
        if output_model.__name__ == RestSchemaTypes.SERIES.value:
            out_name = _get_prop_from_series_schema(output_model)
        else:
            out_name = "value"
        return output_model(**{out_name: value.tolist()})


class SequenceSerializer(ObjectSerializer):
    @classmethod
    def deserialize(cls, value: CustomDeserializingModelT) -> Any:
        return value

    @classmethod
    def serialize(
        cls, value: Union[Sequence, Dict], output_model: Type[BaseModel] = None
    ) -> Union[Dict, List[Dict]]:
        return value


def _get_prop_from_series_schema(schema):
    return list(schema.schema()["properties"].keys())[0]
