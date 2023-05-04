"""Utility functions"""

import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)


def print_metrics(y_true: pd.Series, y_pred: pd.Series) -> None:
    rmse = mean_squared_error(y_true, y_pred, squared=False)

    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)

    print(f"RMSE: {rmse:>10.2f}")
    print(f"MAE: {mae:>11.2f}")
    print(f"MAPE: {mape:>11.2%}")
