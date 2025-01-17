from logging import ERROR, INFO, WARNING, basicConfig, getLogger
from os import environ, getenv
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pandas import read_csv

load_dotenv(override=True)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
getLogger("fontTools").setLevel(ERROR)
getLogger("httpx").setLevel(WARNING)
getLogger("hxl").setLevel(WARNING)
getLogger("numexpr.utils").setLevel(WARNING)
getLogger("pyogrio._io").setLevel(WARNING)

environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
environ["OGR_ORGANIZE_POLYGONS"] = "ONLY_CCW"


def is_bool(value: str) -> bool:
    """Converts string option on env variable to boolean.

    Args:
        value: env varable.

    Returns:
        True if string is truthy.
    """
    return value.lower() in ["yes", "on", "true", "1"]


ATTEMPT = int(getenv("ATTEMPT", "5"))
WAIT = int(getenv("WAIT", "10"))
TIMEOUT = int(getenv("TIMEOUT", "60"))
TIMEOUT_DOWNLOAD = int(getenv("TIMEOUT_DOWNLOAD", "600"))
ADMIN_LEVELS = int(getenv("ADMIN_LEVELS", "5"))
MULTIPROCESSING = not is_bool(getenv("MULTIPROCESSING_DISABLED", "NO"))

EPSG_EQUAL_AREA = 6933
EPSG_WGS84 = 4326
GEOJSON_PRECISION = 6
METERS_PER_KM = 1_000_000
PLOTLY_SIMPLIFY = 0.000_01
POLYGON = "Polygon"
SLIVER_GAP_AREA_KM = 0.000_1
SLIVER_GAP_THINNESS = 0.001
VALID_GEOMETRY = "Valid Geometry"

# NOTE: Could do more with this type, as iso3 and levels keys are required.
type CheckReturnList = list[dict[str, Any]]

cwd = Path(__file__).parent
boundaries_dir = cwd / "../data/boundaries"
boundaries_dir.mkdir(parents=True, exist_ok=True)
attributes_dir = cwd / "../data/attributes"
attributes_dir.mkdir(parents=True, exist_ok=True)
images_dir = cwd / "../data/images"
images_dir.mkdir(parents=True, exist_ok=True)
tables_dir = cwd / "../data/tables"
tables_dir.mkdir(parents=True, exist_ok=True)

official_languages = ["ar", "en", "es", "fr", "ru", "zh"]
romanized_languages = ["en", "es", "fr", "hu", "id", "nl", "pl", "pt", "ro", "sk"]

ignored_iso3 = ["PRI", "JPN", "TJK"]
oversized_areas = {"CHL": [0, 1], "IDN": [0], "PHL": [0, 1, 2]}

metadata_columns = [
    "iso3",
    "iso2",
    "name",
    "itos_url",
    "itos_update",
    "itos_service",
    "itos_level",
    *[f"itos_index_{level}" for level in range(ADMIN_LEVELS + 1)],
    "hdx_url",
    "hdx_date",
    "hdx_update",
    "hdx_source_1",
    "hdx_source_2",
    "hdx_license",
    "hdx_caveats",
]

misc_columns = [
    "OBJECTID",
    "geometry",
    "Shape__Area",
    "Shape__Length",
    "date",
    "validOn",
    "validTo",
    "AREA_SQKM",
]

unterm = {x["iso3"]: x for x in read_csv(cwd / "unterm.csv").to_dict("records")}
m49 = {x["iso3"]: x for x in read_csv(cwd / "m49.csv").to_dict("records")}
