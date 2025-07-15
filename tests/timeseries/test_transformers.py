import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal

from timeseries.transformers import (
    IdentityTransformer,
    SignRetainingFuncTransformer,
    _get_cols,
)

NUM_COLS = ["NumCol1", "NumCol2", "NumCol3"]
STR_COLS = ["StrCol1", "StrCol2"]

np.random.seed(0)


def _get_floats(low: int, high: int, size: int) -> list[float]:
    """Helper function generating list of random floats"""
    return list(np.random.uniform(low=low, high=high, size=size))


def _get_ints(low: int, high: int, size: int) -> list[float]:
    """Helper function generating list of random data"""
    return list(np.random.randint(low=low, high=high, size=size))


@pytest.fixture()
def df1() -> pd.DataFrame:
    data = {
        "Sign": [-1, -1, -1, 1, 1, 1],
        NUM_COLS[0]: [-1, -10, -100, 1, 10, 100],
        NUM_COLS[1]: [-1, -2, -3, 4, 5, np.nan],
        NUM_COLS[2]: [-0.1, -0.2, -0.5, 0.1, 0.2, 0.5],
        STR_COLS[0]: ["A", "A", "B", "C", "C", "C"],
        STR_COLS[1]: ["a", "a", "a", "b", "c", None],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture()
def df2() -> pd.DataFrame:
    data = {
        STR_COLS[0]: ["B", "C", "A", "B", "C", "C"],
        STR_COLS[1]: ["c", None, "a", "b", "c", "c"],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture()
def df2_unknown() -> pd.DataFrame:
    data = {
        STR_COLS[0]: ["B", "C", "A", "B", "F", "F"],
        STR_COLS[1]: ["c", None, "a", "b", "c", "c"],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture()
def df3() -> pd.DataFrame:
    data = {
        "feature1": _get_floats(-1, 0, 100) + _get_floats(0, 1, 900),
        "feature2": _get_floats(1, 0, 100) + _get_floats(10, 20, 900),
        "cat1": _get_ints(-100, 0, 100) + _get_ints(0, 100, 900),
        "cat2": _get_ints(-100, 0, 100) + _get_ints(0, 100, 900),
        "target": [1] * 100 + [0] * 900,
    }
    return pd.DataFrame.from_dict(data)


@pytest.mark.parametrize(
    "trf",
    [
        IdentityTransformer().transform,
        IdentityTransformer().inverse_transform,
        IdentityTransformer().fit_transform,
    ],
)
def test_identity_transformer(df1, trf):
    """Tests trivial identity transformer"""
    assert_frame_equal(trf(df1), df1)


@pytest.mark.parametrize(
    "column_input, cols_expected",
    [
        (None, ["Sign", *NUM_COLS, *STR_COLS]),
        ("Sign", ["Sign"]),
        (NUM_COLS[0], [NUM_COLS[0]]),
        (NUM_COLS, NUM_COLS),
        (STR_COLS, STR_COLS),
    ],
)
def test_get_cols(df1, column_input, cols_expected):
    assert_array_equal(_get_cols(df1, column_input), cols_expected)


@pytest.mark.parametrize("cols", [NUM_COLS, NUM_COLS[:2], [NUM_COLS[2]]])
def test_default_sign_retaining_func_transformer(df1, cols):
    """Tests SignRetainingFuncTransformer for multiple column combinations"""
    expected = df1.copy()
    for c in cols:
        expected[c] = np.log1p(df1[c].abs()) * df1["Sign"]

    # Test transform:
    result = SignRetainingFuncTransformer(cols).transform(df1.copy())
    assert_frame_equal(result, expected, atol=1e6)

    # Subsequent test of inverse-transform:
    inverse_expected = df1.copy()
    inverse_expected[cols] = inverse_expected[cols].astype(float)
    inverse_result = SignRetainingFuncTransformer(cols).inverse_transform(result)
    assert_frame_equal(inverse_result, inverse_expected, atol=1e6)


@pytest.mark.parametrize(
    "func, inverse_func",
    [(np.sin, np.arcsin), (np.cos, np.arccos)],
)
def test_non_default_sign_retaining_func_transformer(df1, func, inverse_func):
    """Tests SignRetainingFuncTransformer with custom function/inverse-function pairs"""

    expected = df1.copy()
    expected["NumCol3"] = func(df1["NumCol3"])
    trf = SignRetainingFuncTransformer(
        columns="NumCol3", func=func, inverse_func=inverse_func
    )

    # Test transform as usual:
    result = trf.transform(df1.copy())
    assert_frame_equal(result, expected, atol=1e6)

    # Subsequent test of inverse-transform:
    inverse_expected = df1.copy()
    inverse_expected["NumCol3"] = inverse_expected["NumCol3"].astype(float)
    inverse_result = trf.inverse_transform(result)
    assert_frame_equal(inverse_result, inverse_expected, atol=1e6)
