"""Preprocesing functions"""

import numpy as np
import pandas as pd


def remove_negative_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove negative values from data frame
    """
    for c in df.columns:
        df = df[df[c] >= 0]
    return df


def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Select columns
    """
    return df[columns]


def time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time features to the dataframe
    """
    df["month"] = df.index.month
    df["week"] = df.index.isocalendar().week
    df["day"] = df.index.day
    df["day_of_week"] = df.index.day_of_week
    df["hour"] = df.index.hour
    df["is_weekend"] = np.where(df["day_of_week"] > 4, 1, 0)
    return df


def lag_features(df: pd.DataFrame, columns: list[str], lags: list[int]) -> pd.DataFrame:
    """
    Add lag features to the dataframe
    """
    for c in columns:
        for h in lags:
            tmp = df[[c]].shift(freq=f"{h}H")
            tmp.columns = [f"{c}_lag_{h}"]
            df = df.merge(tmp, left_index=True, right_index=True, how="left")
    return df


def window_features(
    df: pd.DataFrame, columns: list[str], funcs: list[str] = None
) -> pd.DataFrame:
    if funcs is None:
        funcs = ["mean", "min", "max", "std"]
    tmp = (
        df[columns]
        .rolling(window="5H")
        .agg(funcs)  # Aggregate functions over the span of the window
        .shift(freq="1H")  # Move the average 1 hour forward
    )

    tmp.columns = tmp.columns.map("_win_".join)
    return df.copy().merge(tmp, left_index=True, right_index=True, how="left")


def remove_na(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove NA values from the dataframe
    """
    return df.dropna()
