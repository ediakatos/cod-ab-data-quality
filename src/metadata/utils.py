import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("httpx").setLevel(logging.WARNING)

cwd = Path(__file__).parent

columns = [
    "iso3",
    "iso2",
    "name",
    "itos_url",
    "itos_service",
    "itos_date",
    "itos_update",
    "itos_language_1",
    "itos_language_2",
    "itos_language_3",
    "itos_level",
    "itos_index_0",
    "itos_index_1",
    "itos_index_2",
    "itos_index_3",
    "itos_index_4",
    "hdx_url",
    "hdx_date",
    "hdx_update",
    "hdx_source_1",
    "hdx_source_2",
    "hdx_license",
]


def get_config():
    dtypes = {"admin_level": "Int8", "itos_index": "Int8", "itos_error": str}
    df = pd.read_csv(cwd / "../config.csv", dtype=dtypes)
    return df.to_dict("records")


def join_hdx_metadata(row, hdx):
    row["hdx_date"] = hdx["dataset_date"][1:11]
    row["hdx_update"] = hdx["last_modified"][:10]
    row["hdx_source_1"] = hdx["dataset_source"]
    row["hdx_source_2"] = hdx["organization"]["title"]
    row["hdx_license"] = hdx["license_title"]
    row["hdx_url"] = f"https://data.humdata.org/dataset/cod-ab-{row['iso3'].lower()}"
    return row


def join_itos_metadata(row, itos):
    row["itos_url"] = itos["url"]
    row["itos_service"] = itos["path"]
    row["itos_date"] = itos["date"]
    row["itos_update"] = itos["update"]
    for n in range(3):
        lang = itos["langs"][n] if n < len(itos["langs"]) else None
        row[f"itos_language_{n+1}"] = lang
    row["itos_level"] = list(itos["layers"].keys())[-1]
    for n in range(5):
        row[f"itos_index_{n}"] = itos["layers"].get(n)
    return row