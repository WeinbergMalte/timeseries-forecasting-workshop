import pytest

import numpy as np
import pandas as pd
from numpy.testing import assert_array_equal
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from timeseries.estimators import MultiCategoryEstimator

N = 100


@pytest.fixture()
def df() -> pd.DataFrame:
    np.random.seed(0)

    data_1 = list(np.random.uniform(low=0, high=1, size=N))
    data_2 = list(np.random.uniform(low=1, high=2, size=N))
    data_3 = list(np.random.uniform(low=2, high=3, size=N))

    features = data_1 + data_2 + data_3
    data = {
        "category": [0, 1, 2] * N,
        "feature1": features,
        "feature2": [f * 1.2 for f in features],
        "target": [0 if f < 1 else 1 if f < 2 else 2 for f in features],
    }
    return pd.DataFrame.from_dict(data)


@pytest.mark.parametrize(
    "categories",
    [([0, 1, 2]), ([0, 2]), ([0])],
)
def test_multi_category_estimator(df, categories):
    """
    Tests multi category estimator.

    As the estimator should be perfect given the test data,
    prediction and target should be the same.

    Checks edge-case with single category as well.
    """
    X = df[df["category"].isin(categories)]
    y = X.pop("target")

    clf = RandomForestClassifier(n_estimators=10, random_state=0)
    multimodel = MultiCategoryEstimator(estimator=clf, category_col="category")
    multimodel.fit(X, y)

    y_pred = multimodel.predict(X)
    assert len(multimodel.all_categories) == len(categories)
    assert_array_equal(y_pred, y.astype(float).to_numpy())
