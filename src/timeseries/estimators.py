"""Custom model estimators"""

from typing import Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.utils.validation import check_is_fitted


class MultiCategoryEstimator(TransformerMixin, BaseEstimator):
    """
    Scikit-learn estimator for multiple models split on given categorical value in data.
    Usage example:
        ```
        model = MultiCategoryModel(
            estimator=xgb.XGBClassifier(),
            category_col='MY_CATEGORY'
        )
        model.fit(X_train,y_train, **fit_kwargs)
        ```
    eval_set may be used in fit_kwargs if applicable (e.g. for XGBoost estimators).

    :param estimator: Estimator of scikit-learn api form
    :param category_col: Name of the categorical column to split on
    :param verbose: Print progress
    """

    def __init__(
        self, estimator: BaseEstimator, category_col: str, verbose: bool = False
    ):
        self.estimator = estimator
        self.category_col = category_col
        self.verbose = verbose

    def _fit(
        self, X: pd.DataFrame, y: Union[np.ndarray, pd.Series, pd.DataFrame], **kwargs
    ):
        """
        Fit multi-category models.

        The heavy lifting of the prediction method is moved in here to allow
        for an easy extension of the generic estimator to more specific classifiers.
        """
        self.all_categories = X[self.category_col].unique()
        kwargs_category = kwargs.copy()

        self.estimators = {}
        for category in self.all_categories:
            if self.verbose:
                print(f"Fitting for category: {category}")
            idx = (X[self.category_col] == category).values
            if "eval_set" in kwargs:
                eval_category = []
                for e in kwargs["eval_set"]:
                    X_e, y_e = e
                    idx_e = (X_e[self.category_col] == category).values
                    eval_category.append(
                        (X_e[idx_e].drop([self.category_col], axis=1), y_e[idx_e])
                    )

                kwargs_category["eval_set"] = eval_category
            est = clone(self.estimator)
            self.estimators[category] = est.fit(
                X[idx].drop([self.category_col], axis=1), y[idx], **kwargs_category
            )

        self.is_fitted_ = True
        return self

    def _predict(self, X: pd.DataFrame, y=None) -> np.ndarray:
        """
        Generic estimator prediction.

        The heavy lifting of the prediction method is moved in here to allow
        for an easy extension of the generic estimator to more specific classifiers.
        """
        check_is_fitted(self, "is_fitted_")
        y_preds = np.ones(len(X))
        pred_categories = X[self.category_col].unique()
        for category in pred_categories:
            idx = (X[self.category_col] == category).values
            y_preds[idx] = self.estimators[category].predict(
                X[idx].drop([self.category_col], axis=1)
            )
        return y_preds

    def fit(self, X: pd.DataFrame, y, **kwargs):
        """Fit multi-category models."""
        return self._fit(X, y, **kwargs)

    def predict(self, X: pd.DataFrame, y=None) -> np.ndarray:
        """Predict for each category."""
        return self._predict(X, y=None)
