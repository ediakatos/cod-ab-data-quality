from pandas import DataFrame


def main(checks: DataFrame) -> DataFrame:
    """Scores columns used within dataset.

    Gives a perfect score to layers which have all required name columns (ADM2_EN), with
    no empty cells, no columns all uppercase, no cells lacking alphabetic characters,
    and all characters matching the language code.

    Args:
        checks: checks DataFrame.

    Returns:
        Checks DataFrame with additional columns for scoring.
    """
    scores = checks[["iso3", "level"]].copy()
    scores["table_names"] = (
        checks["name_column_levels"].eq(checks["level"] + 1)
        & checks["name_column_count"].ge(
            checks["language_count"] * (checks["level"] + 1),
        )
        & checks["name_spaces_double"].eq(0)
        & checks["name_spaces_strip"].eq(0)
        & checks["name_empty_column"].eq(0)
        & (
            checks["name_upper_column"].eq(0)
            | checks["name_upper_column"].eq(checks["name_numbers_column"])
        )
        & (
            checks["name_lower_column"].eq(0)
            | checks["name_lower_column"].eq(checks["name_numbers_column"])
        )
        & (
            checks["name_no_valid"].eq(0)
            | checks["name_no_valid"].eq(checks["name_numbers"])
        )
        & checks["name_invalid"].eq(0)
        & checks["name_invalid_adm0"].eq(0)
    )
    return scores
