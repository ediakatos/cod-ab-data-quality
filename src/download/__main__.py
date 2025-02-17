from logging import getLogger
from shutil import which

from tqdm import tqdm

from src.config import ADMIN_LEVELS
from src.utils import get_metadata

from . import httpx, ogr2ogr

logger = getLogger(__name__)


def main() -> None:
    """Downloads all available COD boundary data from ITOS ArcGIS server.

    Uses the metadata.csv sheet generated with a separate module to iterate through each
    ISO-3 country code (AFG, AGO, ARE), getting a list of all admin layers (ADM0, ADM1,
    ADM2, etc), downloading all to a local directory.

    Uses OGR2OGR if available for downloading, as this is faster and more memory
    efficient. If unavailable, fall back to using HTTPX.
    """
    logger.info("Starting")
    download = ogr2ogr.download if which("ogr2ogr") else httpx.download
    records = get_metadata()
    metadata = []
    for record in records:
        metadata.extend(
            {**record, "admin_level": level}
            for level in range(ADMIN_LEVELS + 1)
            if record[f"itos_index_{level}"] is not None
        )
    pbar = tqdm(metadata)
    for row in pbar:
        iso3 = row["iso3"]
        lvl = row["admin_level"]
        idx = row[f"itos_index_{lvl}"]
        pbar.set_postfix_str(f"{iso3}_ADM{lvl}")
        download(iso3, lvl, idx, row["itos_url"])
    logger.info("Finished")


if __name__ == "__main__":
    main()
