"""
Download the DB2 tables used by the assist mapper from wago.tools as CSV.

By default this resolves the latest build for the retail ``wow`` product and
saves each table as ``<Table>.<build>.csv`` in ``data/csv_table``, matching the
filenames wago.tools uses for its own downloads.
"""

import argparse
import logging
import os
import sys
import time

import requests

_logger = logging.getLogger(__name__)

WAGO_BASE_URL = "https://wago.tools"
DEFAULT_OUT_DIR = "data/csv_table"
DEFAULT_PRODUCT = "wow"
TABLES = [
    "AssistedCombat",
    "AssistedCombatRule",
    "AssistedCombatStep",
    "ChrClasses",
    "ChrSpecialization",
    "SpellName",
    "SpellCooldowns",
    "SpellMisc",
    "SpellDuration",
    "SpellCategories",
    "SpellCategory",
]


def get_latest_build(product):
    """Look up the latest build version for a product (e.g. wow, wowt, wow_beta)."""
    response = requests.get(f"{WAGO_BASE_URL}/api/builds/latest", timeout=30)
    response.raise_for_status()
    builds = response.json()
    if product not in builds:
        raise ValueError(f"Unknown product '{product}'; available: {', '.join(sorted(builds))}")
    return builds[product]["version"]


def fetch_table(table, build, out_dir, force=False):
    """Download a single DB2 table as CSV, skipping it if already present."""
    out_file = os.path.join(out_dir, f"{table}.{build}.csv")
    if os.path.exists(out_file) and not force:
        _logger.info(f"{out_file} already exists, skipping")
        return out_file

    url = f"{WAGO_BASE_URL}/db2/{table}/csv"
    _logger.info(f"Downloading {table} for build {build}")
    response = requests.get(url, params={"build": build}, timeout=60)
    response.raise_for_status()
    # wago.tools returns an HTML page instead of CSV for an unknown table/build
    if "text/csv" not in response.headers.get("content-type", ""):
        raise RuntimeError(f"Expected CSV from {response.url}, got {response.headers.get('content-type')}")

    with open(out_file, "wb") as f:
        f.write(response.content)
    return out_file


def parse_args(args):
    parser = argparse.ArgumentParser(description="Download Assisted Combat DB2 tables from wago.tools")
    build_group = parser.add_mutually_exclusive_group()
    build_group.add_argument(
        "-b",
        "--build",
        help="Exact build version to download (e.g. 11.2.0.62493)",
    )
    build_group.add_argument(
        "-p",
        "--product",
        default=DEFAULT_PRODUCT,
        help=f"Product to take the latest build from (default: {DEFAULT_PRODUCT}; e.g. wowt for PTR)",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        default=DEFAULT_OUT_DIR,
        help=f"Directory to save CSVs to (default: {DEFAULT_OUT_DIR})",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Re-download tables even if the file already exists",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    logging.basicConfig(
        level=args.loglevel or logging.WARNING,
        stream=sys.stdout,
        format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    build = args.build or get_latest_build(args.product)
    os.makedirs(args.out_dir, exist_ok=True)

    for table in TABLES:
        print(fetch_table(table, build, args.out_dir, args.force))
        # Be polite to wago.tools
        time.sleep(1)

    print(f"Build: {build}")


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
