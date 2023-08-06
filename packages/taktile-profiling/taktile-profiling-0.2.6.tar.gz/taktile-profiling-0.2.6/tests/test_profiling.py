import shutil
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from tktl import Tktl

from profiling.convenience import (
    BASE_RESULTS_PATH,
    create_accuracy,
    create_dependence,
    create_expectations,
    create_importance,
)

# Generate test data
X = pd.DataFrame.from_dict(
    {
        "Integer": pd.Series([1, 2, 3], dtype="int64"),
        "Float": pd.Series([None, 2.0, 3.0], dtype="float64"),
        "Object": pd.Series([None, "", "c"], dtype="object"),
        "Bool": pd.Series([True, False, True], dtype="bool"),
        "Categorical": pd.Series(["a", "b", None], dtype="category"),
        "Datetime": pd.Series(
            ["2020-01-01", None, "2020-01-03"], dtype="datetime64[ns]"
        ),
    }
)
y_regression = pd.Series([5, 3.2, -0.2], name="Outcome")
y_binary = pd.Series([True, False, True], name="Outcome")

# Instantiate client and generate test endpoints
tktl = Tktl()


@tktl.endpoint(kind="regression", X=X, y=y_regression)
def regression(X):
    return np.random.uniform(size=len(X))


@tktl.endpoint(kind="binary", X=X, y=y_binary)
def binary(X):
    return np.random.uniform(size=len(X))


@tktl.endpoint(kind="binary", X=X, y=y_binary)
def type_sensitive(df):
    assert X.dtypes.equals(df.dtypes)  # ensure types never change during profiling
    return np.random.uniform(size=len(df))


def test_expectations():
    for endpoint in tktl.endpoints:
        name = endpoint.func.__name__
        create_expectations(endpoint)
        for var in X.columns:
            path = Path(BASE_RESULTS_PATH, name, "anatomy", "condexp", var + ".json")
            assert path.exists()
    shutil.rmtree(BASE_RESULTS_PATH)


def test_dependence():
    for endpoint in tktl.endpoints:
        name = endpoint.func.__name__
        create_dependence(endpoint)
        for var in X.columns:
            path = Path(BASE_RESULTS_PATH, name, "anatomy", "partialdep", var + ".json")
            assert path.exists()
    shutil.rmtree(BASE_RESULTS_PATH)


def test_importance():
    for endpoint in tktl.endpoints:
        name = endpoint.func.__name__
        create_importance(endpoint)
        assert Path(BASE_RESULTS_PATH, name, "anatomy", "varimp.json").exists()
    shutil.rmtree(BASE_RESULTS_PATH)


def test_accuracy():
    for endpoint in tktl.endpoints:
        name = endpoint.func.__name__
        create_accuracy(endpoint)
        assert Path(BASE_RESULTS_PATH, name, "accuracy", "calibration.json").exists()
        assert Path(BASE_RESULTS_PATH, name, "accuracy", "metrics.json").exists()
        assert Path(BASE_RESULTS_PATH, name, "accuracy", "errors.json").exists()
    shutil.rmtree(BASE_RESULTS_PATH)
