"""Module containing custom scikit-learn transformers."""

from typing import Callable, Optional, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from timeseries.utils import ensure_iterable


def _get_cols(X, cols):
    """Get passed columns as list or all columns of input data if none are provided."""
    cols = None if not cols else ensure_iterable(cols)
    return cols if cols else X.columns


class IdentityTransformer(BaseEstimator, TransformerMixin):
    """Does nothing."""

    def __init__(self):
        pass

    def fit(self, X: Union[pd.DataFrame, np.ndarray], y=None):
        """Fit."""
        return self

    def transform(
        self, X: Union[pd.DataFrame, np.ndarray]
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Transform."""
        return X

    def inverse_transform(
        self, X: Union[pd.DataFrame, np.ndarray]
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Inverse transform."""
        return X


class SignRetainingFuncTransformer(BaseEstimator, TransformerMixin):
    """
    Function transformer acting on subset of columns while retaining
    the sign of values.
    This can be particularly useful for target/feature-engineering
    for algorithms that are sensitive to outliers.

    Default behavior:
        Transforms values to numpy.log1p with negative values retaining their sign
        Inverse transform applies numpy.expm1

    :param columns: Name or list of names of column(s) to transform
        If not provided, the transformation is applied to the whole dataset
    :param func: Transformation function to be applied, default np.log1p
    :param inverse_func: Inverse function of func, default np.expm1
    """

    def __init__(
        self,
        columns: Optional[Union[str, list[str]]] = None,
        func: Callable = np.log1p,
        inverse_func: Callable = np.expm1,
    ):
        self.func = func
        self.inverse_func = inverse_func
        self.columns = columns

    def fit(self, X: pd.DataFrame, y=None):
        """Fit."""
        return self

    def _func_transform(self, X: pd.DataFrame, func: Callable) -> pd.DataFrame:
        """Transforms data with function `func` while retaining their sign."""
        for col in _get_cols(X, self.columns):
            X[col] = func(X[col].abs()) * np.sign(X[col])
        return X

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform."""
        return self._func_transform(X, self.func)

    def inverse_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Inverse transform."""
        return self._func_transform(X, self.inverse_func)
