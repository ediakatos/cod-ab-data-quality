from dateutil.relativedelta import relativedelta
from pandas import DataFrame, Timestamp


def main(checks: DataFrame) -> DataFrame:
    """Function for scoring date values within dataset.

    Gives a perfect score if there is only one date value for the "date" and "validOn"
    columns, as well as whether the "validOn" column is less than 1 year. OCHA conducts
    an annual COD review process where datasets should be validated on a 12 month cycle.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["date"] = checks["date_count"].eq(1)
    scores["valid_on"] = (
        checks["update_count"].eq(1)
        & checks["update_1"].gt(Timestamp.now() - relativedelta(years=1))
        & checks["valid_to_exists"].eq(1)
        & checks["valid_to_empty"].eq(1)
    )
    return scores
