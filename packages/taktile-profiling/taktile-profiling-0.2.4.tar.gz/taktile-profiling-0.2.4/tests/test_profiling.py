import shutil
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from tktl import Tktl

from profiling.convenience import (
    create_accuracy,
    create_dependence,
    create_expectations,
    create_importance, BASE_RESULTS_PATH
)

# Generate test data
X = pd.DataFrame.from_dict(
    {
        "Integer": [1, 2, 3],
        "Float": [None, 2.0, 3.0],
        "Object": [None, "", "c"],
        "Categorical": ["a", "b", "c"],
        "Date": [date(2020, 1, 1), date(2020, 1, 2), date(2020, 1, 3)],
        "Datetime": [datetime(2020, 1, 1), None, datetime(2020, 1, 3)],
    }
).astype({"Categorical": "category"})
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
