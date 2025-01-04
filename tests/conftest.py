from pathlib import Path
from typing import Literal

import pytest
from geopandas import GeoDataFrame, read_parquet


@pytest.fixture(scope="session")
def iso3() -> Literal["MDG"]:
    """Fixture to load test data."""
    return "MDG"


@pytest.fixture(scope="session")
def gdfs() -> list[GeoDataFrame]:
    """Fixture to load test data."""
    test_data_dir = Path("tests/test_data")
    file_paths = sorted(test_data_dir.glob("*.parquet"))
    return [read_parquet(x) for x in file_paths]
