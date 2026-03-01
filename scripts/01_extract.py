"""
    Script to extract AirNow data files for a range of dates.

    This script downloads hourly air quality observation data and monitoring
    site location data from the EPA's AirNow program. Files are saved into
    a date-organized folder structure under data/raw/.

    AirNow files are hosted at:
        https://files.airnowtech.org/?prefix=airnow/

    Usage:
        python scripts/01_extract.py
"""

import pathlib
import urllib.request
import shutil


DATA_DIR = pathlib.Path(__file__).parent.parent / 'data'
BASE_URL = "https://s3-us-west-1.amazonaws.com/files.airnowtech.org/airnow"


def download_data_for_date(date_str):
    """Download AirNow data files for a single date.

    Downloads all 24 HourlyData files (hours 00-23) and the
    Monitoring_Site_Locations_V2.dat file for the specified date,
    saving them into data/raw/YYYY-MM-DD/.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format. For example, '2024-07-01'.
    """
    date_obj = datetime.date.fromisoformat(date_str)
    yyyy = str(date_obj.year)
    yyyymmdd = date_obj.strftime("%Y%m%d")

    out_dir = DATA_DIR / "raw" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)

    # 24 hourly files
    for hh in range(24):
        hh_str = f"{hh:02d}"
        fname = f"HourlyData_{yyyymmdd}{hh_str}.dat"
        url = f"{BASE_URL}/{yyyy}/{yyyymmdd}/{fname}"
        dest = out_dir / fname

        if dest.exists() and dest.stat().st_size > 0:
            continue

        with urllib.request.urlopen(url) as resp, open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)

    # site locations file
    sites_fname = "Monitoring_Site_Locations_V2.dat"
    sites_url = f"{BASE_URL}/{yyyy}/{yyyymmdd}/{sites_fname}"
    sites_dest = out_dir / sites_fname

    if not (sites_dest.exists() and sites_dest.stat().st_size > 0):
        with urllib.request.urlopen(sites_url) as resp, open(sites_dest, "wb") as f:
            shutil.copyfileobj(resp, f)


if __name__ == '__main__':
    import datetime

    # Download data for July 2024
    start_date = datetime.date(2024, 7, 1)
    end_date = datetime.date(2024, 7, 31)

    current_date = start_date
    while current_date <= end_date:
        print(f'Downloading data for {current_date}...')
        download_data_for_date(current_date.isoformat())
        current_date += datetime.timedelta(days=1)

    print('Done.')
