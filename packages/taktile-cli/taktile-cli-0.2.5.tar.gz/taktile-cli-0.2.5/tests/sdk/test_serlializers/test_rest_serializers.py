import pandas
from numpy.testing import assert_array_equal

from pydantic import BaseModel

from tktl.core.serializers import to_pydantic
from tktl.core.serializers.rest import DataFrameSerializer, SeriesSerializer


def test_frame_serializer(serializer_df_inputs: pandas.DataFrame):
    model = to_pydantic(serializer_df_inputs)
    as_pydantic_model = DataFrameSerializer.serialize(serializer_df_inputs, output_model=model)
    assert isinstance(as_pydantic_model, list)
    assert as_pydantic_model[0].index == serializer_df_inputs.index.values[0]
    serialized = model.parse_obj(serializer_df_inputs.to_dict('recods'))
    deser = serialized.deserialize()
    assert isinstance(deser, pandas.DataFrame)
    assert list(deser.columns) == list(serializer_df_inputs.columns)
    assert_array_equal(deser['A'].values, serializer_df_inputs['A'].values)
    assert set(serializer_df_inputs.columns.tolist()).issubset(set(serialized.dict()['__root__'][0].keys()))


def test_series_serializer(serializer_series_inputs: pandas.Series):
    model = to_pydantic(serializer_series_inputs)
    as_pydantic_model = SeriesSerializer.serialize(serializer_series_inputs, output_model=model)
    assert isinstance(as_pydantic_model, BaseModel)
    assert isinstance(as_pydantic_model.dict()["B"], list)
