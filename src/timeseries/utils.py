"""Utility functions"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)


def print_metrics(y_true: pd.Series, y_pred: pd.Series) -> None:
    """
    Print some interesting metrics in a nicely readable format

    :param y_true: True values
    :param y_pred: Predicted values
    """
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)

    print(f"RMSE: {rmse:>10.2f}")
    print(f"MAE: {mae:>11.2f}")
    print(f"MAPE: {mape:>11.2%}")


def ensure_iterable(x: Any) -> Iterable[Any]:
    """
    Returns a list with single-element x if x is a string or not iterable already.
    note that, while strings and bytes are iterable as well, we exclude them here.

    :param x: any input where itreable-ness should be ensured.
    :return: x or list with single element x if and only if x wasn't already an iterable (or a string or bytes).
    """
    if isinstance(x, (str, bytes)):
        return [x]
    try:
        iter(x)
        return x
    except TypeError:
        return [x]
