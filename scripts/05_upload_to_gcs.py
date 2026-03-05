"""
    Script to re-upload prepared data to GCS using hive-partitioned folder structure.

    This script takes the same prepared files from Part 2 and uploads them
    to GCS with a hive-partitioned directory layout. Instead of flat files like:
        air_quality/hourly/2024-07-01.csv

    Files are organized as:
        air_quality/hourly/csv/airnow_date=2024-07-01/data.csv

    This enables BigQuery to automatically detect the partition key
    (airnow_date) and use it for query pruning, so queries filtering
    by date only scan the relevant files.

    This is a backfill of the upload step — you don't need to re-download
    or re-transform anything. You're just re-uploading the same files
    with a different folder structure.

    Prerequisites:
        - Run `gcloud auth application-default login` to authenticate.
        - Parts 1-3 should be complete (data already prepared and uploaded once).

    Usage:
        python scripts/05_upload_to_gcs.py
"""

import pathlib
from google.cloud import storage

DATA_DIR = pathlib.Path(__file__).parent.parent / 'data'

# TODO: Update this to your bucket name
BUCKET_NAME = 'sihanyu_musa_5090'
PROJECT_ID = "musa-geocloud-sihan"

def upload_with_hive_partitioning():
    """Upload prepared hourly data to GCS with hive-partitioned folder structure.

    For each date's prepared files, upload them to GCS with the following
    folder structure:
        gs://<bucket>/air_quality/hourly/csv/airnow_date=2024-07-01/data.csv
        gs://<bucket>/air_quality/hourly/jsonl/airnow_date=2024-07-01/data.jsonl
        gs://<bucket>/air_quality/hourly/parquet/airnow_date=2024-07-01/data.parquet

    The site locations files don't need hive partitioning (they're not
    date-partitioned), so you can re-upload them as-is or skip them.
    """
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)

    prepared_hourly = DATA_DIR / 'prepared' / 'hourly'

    for csv_file in sorted(prepared_hourly.glob('*.csv')):
        date_str = csv_file.stem
        print(f'Uploading {date_str}...')

        # CSV
        blob = bucket.blob(f'air_quality/hourly/csv/airnow_date={date_str}/data.csv')
        blob.upload_from_filename(csv_file)

        # JSONL
        jsonl_file = prepared_hourly / f'{date_str}.jsonl'
        if jsonl_file.exists():
            blob = bucket.blob(f'air_quality/hourly/jsonl/airnow_date={date_str}/data.jsonl')
            blob.upload_from_filename(jsonl_file)

        # Parquet
        parquet_file = prepared_hourly / f'{date_str}.parquet'
        if parquet_file.exists():
            blob = bucket.blob(f'air_quality/hourly/parquet/airnow_date={date_str}/data.parquet')
            blob.upload_from_filename(parquet_file)

    print('All hourly files uploaded with hive partitioning.')


if __name__ == '__main__':
    upload_with_hive_partitioning()
    print('Done.')
