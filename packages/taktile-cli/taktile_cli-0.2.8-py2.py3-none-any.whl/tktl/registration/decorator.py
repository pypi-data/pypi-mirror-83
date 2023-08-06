import functools
import warnings
from abc import ABC, abstractmethod
from typing import Any, Callable, Tuple, Union

import pandas

from tktl.core.exceptions import exceptions
from tktl.core.loggers import CliLogger
from tktl.core.t import EndpointKinds
from tktl.registration.schema import EndpointInputSchema, EndpointOutputSchema
from tktl.registration.validation import (
    validate_binary,
    validate_outputs,
    validate_shapes,
)

logger = CliLogger()


class Endpoint(ABC):
    KIND: str
    input_schema: EndpointInputSchema
    output_schema: EndpointOutputSchema

    def __init__(self, func: Callable):
        self._func = func

    @property
    def func(self):
        return self._func

    @property
    def profile_func(self) -> Union[Any, pandas.Series]:
        name = self._func.__name__

        def to_series(x):
            return pandas.Series(self.func(x))

        to_series.__name__ = name
        return to_series

    @property
    @abstractmethod
    def profiling_supported(self):
        return True

    @abstractmethod
    def get_input_and_output_for_profiling(
        self,
    ) -> Tuple[pandas.DataFrame, pandas.Series]:
        raise NotImplementedError

    @property
    def input_names(self):
        return []

    @property
    def output_names(self):
        return []


class TabularEndpoint(Endpoint):
    KIND: str = EndpointKinds.TABULAR

    def __init__(self, func, X, y):
        super().__init__(func)
        self.input_schema = EndpointInputSchema(
            value=X, endpoint_kind=self.KIND, endpoint_name=self.func.__name__
        )
        self.output_schema = EndpointOutputSchema(
            value=y, endpoint_kind=self.KIND, endpoint_name=self.func.__name__
        )

    def _profiling_supported(self) -> Union[bool, pandas.Series]:
        if (
            not self.input_schema.pandas_convertible
            and not self.output_schema.pandas_convertible
        ):

            return False
        try:
            predictions = self.func(self.input_schema.value)
        except Exception as e:
            raise exceptions.ValidationException(
                f"Function provided is unable to produce predictions from given sample values: {e}"
            )
        return predictions

    @property
    def profiling_supported(self):
        predictions = self._profiling_supported()
        if predictions is False:
            return False
        else:
            try:
                x_frame = self.input_schema.get_pandas_representation()
                y_series = self.output_schema.get_pandas_representation()
            except ValueError:
                return False
            return validate_outputs(predictions) and validate_shapes(
                x_frame, y_series, predictions
            )

    @property
    def input_names(self):
        return self.input_schema.names

    @property
    def output_names(self):
        return self.output_schema.names

    def get_input_and_output_for_profiling(
        self,
    ) -> Tuple[pandas.DataFrame, pandas.Series]:
        return self._drop_missing_values()

    def _drop_missing_values(self) -> Tuple[pandas.DataFrame, pandas.Series]:
        x = self.input_schema.get_pandas_representation()
        y = self.output_schema.get_pandas_representation()
        not_missing = [i for i, v in enumerate(y) if not pandas.isna(v)]
        n_missing = len(y) - len(not_missing)
        if n_missing > 0:
            warnings.warn(f"y contains {n_missing} missing values that will be dropped")
            return x.iloc[not_missing], y.iloc[not_missing]
        else:
            return x, y


class BinaryEndpoint(TabularEndpoint):
    KIND = EndpointKinds.BINARY

    def __init__(self, func, X, y):
        super().__init__(func, X, y)

    @property
    def profiling_supported(self):
        predictions = self._profiling_supported()
        if predictions is False:
            return False
        return super().profiling_supported and validate_binary(predictions)


class RegressionEndpoint(TabularEndpoint):
    KIND = EndpointKinds.REGRESSION

    def __init__(self, func, X, y):
        super().__init__(func, X, y)

    @property
    def profiling_supported(self):
        predictions = self._profiling_supported()
        if predictions is False:
            return False
        return super().profiling_supported and validate_outputs(predictions)


class CustomEndpoint(Endpoint):
    def get_input_and_output_for_profiling(
        self,
    ) -> Tuple[pandas.DataFrame, pandas.Series]:
        raise ValueError("Custom endpoint does not have profiling enabled")

    KIND = EndpointKinds.CUSTOM

    def __init__(self, func, payload_model=None, response_model=None):
        super().__init__(func)
        try:
            assert isinstance(func, Callable)
        except AssertionError:
            raise exceptions.ValidationException("Endpoint function is not a callable")
        self.payload_model = payload_model
        self.response_model = response_model

    @property
    def profiling_supported(self):
        return False


class Tktl:
    def __init__(self):
        self.endpoints = []

    # This is the user-facing decorator for function registration
    def endpoint(
        self,
        func: Callable = None,
        kind: str = EndpointKinds.REGRESSION,
        X: Any = None,
        y: Any = None,
        payload_model=None,
        response_model=None,
    ):
        """Register function as a Taktile endpoint

        Parameters
        ----------
        func : Callable, optional
            Function that describes the desired operation, by default None
        kind : str, optional
            Specification of endpoint type ("regression", "binary", "custom"),
            by default "regression"
        X : pd.DataFrame, optional
            Reference input dataset for testing func. Used when argument "kind"
            is set to "regression" or "binary", by default None.
        y : pd.Series, optional
            Reference output for evaluating func. Used when argument "kind"
            is set to "regression" or "binary", by default None.
        payload_model:
            Type hint used for documenting and validating payload. Used in
            custom endpoints only.
        response_model:
            Type hint used for documenting and validating response. Used in
            custom endpoints only.

        Returns
        -------
        Callable
            Wrapped function
        """
        if func is None:
            return functools.partial(
                self.endpoint,
                kind=kind,
                X=X,
                y=y,
                payload_model=payload_model,
                response_model=response_model,
            )

        if kind == "tabular":
            endpoint = TabularEndpoint(func=func, X=X, y=y)
        elif kind == "regression":
            endpoint = RegressionEndpoint(func=func, X=X, y=y)
        elif kind == "binary":
            endpoint = BinaryEndpoint(func=func, X=X, y=y)
        elif kind == "custom":
            endpoint = CustomEndpoint(
                func=func, payload_model=payload_model, response_model=response_model
            )
        else:
            raise exceptions.ValidationException(f"Unknown endpoint kind: '{kind}'")

        self.endpoints.append(endpoint)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pred = func(*args, **kwargs)
            return pred

        return wrapper
