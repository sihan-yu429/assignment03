"""
    Script to upload prepared data files to Google Cloud Storage (GCS).

    This script uploads the transformed files from data/prepared/ to a
    GCS bucket, preserving the folder structure so that BigQuery can
    use wildcard URIs to create external tables across multiple files.

    Prerequisites:
        - Run `gcloud auth application-default login` to authenticate.
        - Create a GCS bucket (manually or in this script).

    Usage:
        python scripts/03_upload_to_gcs.py
"""

import pathlib
from google.cloud import storage


DATA_DIR = pathlib.Path(__file__).parent.parent / 'data'

# TODO: Update this to your bucket name
BUCKET_NAME = 'sihanyu_musa_5090'
PROJECT_ID = "musa-geocloud-sihan"


def upload_prepared_data():
    """Upload all prepared data files to GCS.

    Uploads the contents of data/prepared/ to the GCS bucket,
    preserving the folder structure under a prefix of 'air_quality/'.

    Expected GCS structure:
        gs://<bucket>/air_quality/hourly/2024-07-01.csv
        gs://<bucket>/air_quality/hourly/2024-07-01.jsonl
        gs://<bucket>/air_quality/hourly/2024-07-01.parquet
        ...
        gs://<bucket>/air_quality/sites/site_locations.csv
        gs://<bucket>/air_quality/sites/site_locations.jsonl
        gs://<bucket>/air_quality/sites/site_locations.geoparquet
    """
    prepared_dir = DATA_DIR / "prepared"
    if not prepared_dir.exists():
        raise RuntimeError("data/prepared/ not found. Run scripts/02_prepare.py first.")

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)

    for local_path in prepared_dir.rglob("*"):
        if local_path.is_dir():
            continue

        # relative path from data/prepared/
        rel_path = local_path.relative_to(prepared_dir).as_posix()  
        blob_path = f"air_quality/{rel_path}"                      

        blob = bucket.blob(blob_path)
        blob.upload_from_filename(str(local_path))

        print(f"Uploaded: gs://{BUCKET_NAME}/{blob_path}")

if __name__ == '__main__':
    upload_prepared_data()
    print('Done.')