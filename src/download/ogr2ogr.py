from logging import getLogger
from re import compile
from subprocess import DEVNULL, run
from time import sleep

from tenacity import retry, stop_after_attempt, wait_fixed

from .utils import ATTEMPT, WAIT, outputs

logger = getLogger(__name__)


def ogr2ogr(idx: int, url: str, filename: str, records: int | None):
    query = "f=json&where=1=1&outFields=*&orderByFields=OBJECTID"
    record_count = f"&resultRecordCount={records}" if records is not None else ""
    return run(
        [
            "ogr2ogr",
            "-overwrite",
            *["--config", "OGR_GEOJSON_MAX_OBJ_SIZE", "0"],
            *["-nln", filename],
            *["-oo", "FEATURE_SERVER_PAGING=YES"],
            outputs / f"{filename}.gpkg",
            f"{url}/{idx}/query?{query}{record_count}",
        ],
        stderr=DEVNULL,
    )


def is_valid(file):
    regex = compile(r"\((Multi Polygon|Polygon)\)")
    result = run(["ogrinfo", file], capture_output=True)
    return regex.search(result.stdout.decode("utf-8"))


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def download(iso3: str, lvl: int, idx: int, url: str):
    filename = f"{iso3}_adm{lvl}".lower()
    success = False
    for records in [None, 1000, 100, 10, 1]:
        result = ogr2ogr(idx, url, filename, records)
        if result.returncode == 0:
            success = True
            break
        else:
            sleep(WAIT)
    if success:
        if not is_valid(outputs / f"{filename}.gpkg"):
            (outputs / f"{filename}.gpkg").unlink()
            logger.info(f"NOT VALID POLYGON: {filename}")
    else:
        raise Exception