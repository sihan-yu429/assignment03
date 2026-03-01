"""
    Script to transform raw AirNow data files into BigQuery-compatible formats.

    This script reads the raw .dat files downloaded by 01_extract.py and converts
    them into CSV, JSON-L, and Parquet formats suitable for loading into
    BigQuery as external tables.

    Hourly observation data is converted to: CSV, JSON-L, Parquet
    Site location data is converted to: CSV, JSON-L, GeoParquet (with point geometry)

    Usage:
        python scripts/02_prepare.py
"""

import pathlib
import pandas as pd
import geopandas as gpd



DATA_DIR = pathlib.Path(__file__).parent.parent / 'data'

HOURLY_COLUMNS = [
    'valid_date',
    'valid_time',
    'aqsid',
    'site_name',
    'gmt_offset',
    'parameter_name',
    'reporting_units',
    'value',
    'data_source',
]


# --- Hourly observation data ---

def prepare_hourly_csv(date_str):
    """Convert raw hourly .dat files for a date to a single CSV file.

    Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
    combines them into a single dataset, assigns column names,
    and writes to data/prepared/hourly/<date>.csv.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raw_dir = DATA_DIR / "raw" / date_str
    out_dir = DATA_DIR / "prepared" / "hourly"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("HourlyData_*.dat"))
    if not files:
        raise FileNotFoundError(f"No HourlyData_*.dat files found in {raw_dir}")

    dfs = []
    for fp in files:
        df = pd.read_csv(fp, sep="|", header=None, names=HOURLY_COLUMNS, dtype=str, encoding='latin-1')
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    
    out_path = out_dir / f"{date_str}.csv"
    df_all.to_csv(out_path, index=False)

def prepare_hourly_jsonl(date_str):
    """Convert raw hourly .dat files for a date to newline-delimited JSON.

    Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
    combines them, and writes one JSON object per line to
    data/prepared/hourly/<date>.jsonl.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raw_dir = DATA_DIR / "raw" / date_str
    out_dir = DATA_DIR / "prepared" / "hourly"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("HourlyData_*.dat"))
    if not files:
        raise FileNotFoundError(f"No HourlyData_*.dat files found in {raw_dir}")

    dfs = []
    for fp in files:
        df = pd.read_csv(fp, sep="|", header=None, names=HOURLY_COLUMNS, dtype=str, encoding='latin-1')
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    df_all["value"] = pd.to_numeric(df_all["value"], errors="coerce")
    df_all["gmt_offset"] = pd.to_numeric(df_all["gmt_offset"], errors="coerce")

    out_path = out_dir / f"{date_str}.jsonl"
    df_all.to_json(out_path, orient="records", lines=True)


def prepare_hourly_parquet(date_str):
    """Convert raw hourly .dat files for a date to Parquet format.

    Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
    combines them, and writes to data/prepared/hourly/<date>.parquet.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raw_dir = DATA_DIR / "raw" / date_str
    out_dir = DATA_DIR / "prepared" / "hourly"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("HourlyData_*.dat"))
    if not files:
        raise FileNotFoundError(f"No HourlyData_*.dat files found in {raw_dir}")

    dfs = []
    for fp in files:
        df = pd.read_csv(fp, sep="|", header=None, names=HOURLY_COLUMNS, dtype=str, encoding='latin-1')
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    df_all["value"] = pd.to_numeric(df_all["value"], errors="coerce")
    df_all["gmt_offset"] = pd.to_numeric(df_all["gmt_offset"], errors="coerce")

    out_path = out_dir / f"{date_str}.parquet"
    df_all.to_parquet(out_path, index=False)


# --- Site location data ---

def prepare_site_locations_csv():
    """Convert monitoring site locations to CSV.

    Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
    so there is one row per site (the raw file has one row per
    site-parameter combination), and writes to
    data/prepared/sites/site_locations.csv.

    Use the most recent date's file from data/raw/.
    """
    raw_root = DATA_DIR / "raw"
    out_dir = DATA_DIR / "prepared" / "sites"
    out_dir.mkdir(parents=True, exist_ok=True)

    date_dirs = sorted([p for p in raw_root.iterdir() if p.is_dir()])
    if not date_dirs:
        raise FileNotFoundError(f"No date folders found under {raw_root}")

    # most recent by folder name (YYYY-MM-DD sorts correctly)
    latest_dir = date_dirs[-1]
    fp = latest_dir / "Monitoring_Site_Locations_V2.dat"
    if not fp.exists():
        raise FileNotFoundError(f"Site locations file not found: {fp}")

    df = pd.read_csv(fp, sep="|", header=0, dtype=str, encoding='latin-1')

    # deduplicate: one row per site
    if "AQSID" not in df.columns:
        raise ValueError("AQSID column not found in site locations file.")
    df = df.drop_duplicates(subset=["AQSID"], keep="first").reset_index(drop=True)

    out_path = out_dir / "site_locations.csv"
    df.to_csv(out_path, index=False)



def prepare_site_locations_jsonl():
    """Convert monitoring site locations to newline-delimited JSON.

    Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
    so there is one row per site (the raw file has one row per
    site-parameter combination), and writes to
    data/prepared/sites/site_locations.jsonl.

    Use the most recent date's file from data/raw/.
    """
    raw_root = DATA_DIR / "raw"
    out_dir = DATA_DIR / "prepared" / "sites"
    out_dir.mkdir(parents=True, exist_ok=True)

    date_dirs = sorted([p for p in raw_root.iterdir() if p.is_dir()])
    if not date_dirs:
        raise FileNotFoundError(f"No date folders found under {raw_root}")

    latest_dir = date_dirs[-1]
    fp = latest_dir / "Monitoring_Site_Locations_V2.dat"
    if not fp.exists():
        raise FileNotFoundError(f"Site locations file not found: {fp}")

    df = pd.read_csv(fp, sep="|", header=0, dtype=str, encoding='latin-1')

    if "AQSID" not in df.columns:
        raise ValueError("AQSID column not found in site locations file.")
    df = df.drop_duplicates(subset=["AQSID"], keep="first").reset_index(drop=True)

    out_path = out_dir / "site_locations.jsonl"
    df.to_json(out_path, orient="records", lines=True)
    

def prepare_site_locations_geoparquet():
    """Convert monitoring site locations to GeoParquet with point geometry.

    Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
    so there is one row per site (the raw file has one row per
    site-parameter combination), creates point geometries from
    latitude and longitude, and writes to
    data/prepared/sites/site_locations.geoparquet.

    Use the most recent date's file from data/raw/.
    """
    raw_root = DATA_DIR / "raw"
    out_dir = DATA_DIR / "prepared" / "sites"
    out_dir.mkdir(parents=True, exist_ok=True)

    date_dirs = sorted([p for p in raw_root.iterdir() if p.is_dir()])
    if not date_dirs:
        raise FileNotFoundError(f"No date folders found under {raw_root}")

    latest_dir = date_dirs[-1]
    fp = latest_dir / "Monitoring_Site_Locations_V2.dat"
    if not fp.exists():
        raise FileNotFoundError(f"Site locations file not found: {fp}")

    df = pd.read_csv(fp, sep="|", header=0, dtype=str, encoding='latin-1')

    if "AQSID" not in df.columns:
        raise ValueError("AQSID column not found in site locations file.")
    df = df.drop_duplicates(subset=["AQSID"], keep="first").reset_index(drop=True)

    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        raise ValueError("Latitude/Longitude columns not found in site locations file.")

    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]),
        crs="EPSG:4326",
    )

    out_path = out_dir / "site_locations.geoparquet"
    gdf.to_parquet(out_path, index=False)


if __name__ == '__main__':
    import datetime

    # Prepare site locations (only need to do this once)
    print('Preparing site locations...')
    prepare_site_locations_csv()
    prepare_site_locations_jsonl()
    prepare_site_locations_geoparquet()

    # Prepare hourly data for each day in July 2024 (backfill)
    start_date = datetime.date(2024, 7, 1)
    end_date = datetime.date(2024, 7, 31)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.isoformat()
        print(f'Preparing hourly data for {date_str}...')
        prepare_hourly_csv(date_str)
        prepare_hourly_jsonl(date_str)
        prepare_hourly_parquet(date_str)
        current_date += datetime.timedelta(days=1)

    print('Done.')
