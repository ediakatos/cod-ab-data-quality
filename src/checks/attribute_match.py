from geopandas import GeoDataFrame

from src.config import CheckReturnList
from src.utils import get_name_columns, get_pcode_columns


def main(iso3: str, gdfs: list[GeoDataFrame]) -> CheckReturnList:
    """Check completeness of an admin boundary by checking the columns.

    Args:
        iso3: ISO3 code of the current location being checked.
        gdfs: List of GeoDataFrames, with the item at index 0 corresponding to admin
        level 0, index 1 to admin level 1, etc.

    Returns:
        List of check rows to be outputed as a CSV.
    """
    check_results = []
    for admin_level, gdf in enumerate(gdfs):
        row = {
            "iso3": iso3,
            "level": admin_level,
            "pcode_mismatch": 0,
            "name_mismatch": 0,
        }
        if admin_level > 0:
            parent = gdfs[admin_level - 1]
            pcode_columns = get_pcode_columns(gdf, admin_level - 1)
            name_columns = get_name_columns(gdf, admin_level - 1)
            pcode_columns = [x for x in pcode_columns if x in parent.columns]
            name_columns = [x for x in name_columns if x in parent.columns]
            if len(pcode_columns):
                merged = gdf.merge(parent, on=pcode_columns, how="left", indicator=True)
                row["pcode_mismatch"] = (~merged["_merge"].eq("both")).sum()
            if len(name_columns):
                merged = gdf.merge(parent, on=name_columns, how="left", indicator=True)
                row["name_mismatch"] = (~merged["_merge"].eq("both")).sum()
        check_results.append(row)
    return check_results
