from geopandas import GeoDataFrame

from src.config import CheckReturnList


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Checks for unique date values within dataset.

    There are two date fields within each COD-AB, "date" and "validOn". "date"
    represents when the current boundaries went into effect for the specified location.
    "validOn" represents when this dataset was last changed throughout the data update
    lifecycle. If there are multiple unique values for dates within the dataset, they
    will be listed in separate output columns: "date_1", "date_2", etc.

    The following are a list of source and output columns:
    - source: "date"
        - output: "date_count", "date_1", "date_2", etc...
    - source: "validOn"
        - output: "update_count", "update_1", "update_2", etc...

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of results from this check to output as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        row = {
            "iso3": iso3,
            "level": admin_level,
            "valid_to_exists": 0,
            "valid_to_empty": 0,
            "date_count": 0,
            "update_count": 0,
        }
        try:
            gdf_date = gdf[~gdf["date"].isna()]["date"].drop_duplicates()
            for index, value in enumerate(gdf_date):
                row["date_count"] += 1
                row[f"date_{index+1}"] = value
            gdf_update = gdf[~gdf["validOn"].isna()]["validOn"].drop_duplicates()
            for index, value in enumerate(gdf_update):
                row["update_count"] += 1
                row[f"update_{index+1}"] = value
        except KeyError:
            pass
        if "validTo" in gdf.columns:
            row["valid_to_exists"] = 1
            if gdf["validTo"].isna().all():
                row["valid_to_empty"] = 1
        check_results.append(row)
    return check_results
