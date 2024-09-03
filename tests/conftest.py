import polars as pl
import pytest
from great_tables import GT


@pytest.fixture
def df():
    return pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})


@pytest.fixture
def gtbl(df):
    return GT(df)
