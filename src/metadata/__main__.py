import logging

import httpx
import pandas as pd
from tqdm import tqdm

from .getters import get_hdx_metadata, get_itos_metadata
from .utils import columns, cwd, join_hdx_metadata, join_itos_metadata


def get_metadata():
    url = "https://vocabulary.unocha.org/json/beta-v4/countries.json"
    with httpx.Client(http2=True, timeout=60) as client:
        metadata = client.get(url).json()["data"]
    metadata = filter(lambda x: x["iso3"] is not None, metadata)
    metadata = list(sorted(metadata, key=lambda x: x["iso3"]))
    pbar = tqdm(metadata)
    for row in pbar:
        pbar.set_postfix_str(row["iso3"])
        row["name"] = row["label"]["default"]
        hdx = get_hdx_metadata(row["iso3"])
        if hdx is not None:
            row = join_hdx_metadata(row, hdx)
        itos = get_itos_metadata(row["iso3"])
        if itos is not None:
            row = join_itos_metadata(row, itos)
    return metadata


def save_metadata(metadata):
    df = pd.DataFrame(metadata)
    df = df[df["hdx_date"].notna()]
    df = df[columns]
    dest = cwd / "../../data/metadata.csv"
    df.to_csv(dest, encoding="utf-8-sig", float_format="%.0f", index=False)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("starting")
    metadata = get_metadata()
    save_metadata(metadata)
    logger.info("finished")