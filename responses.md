# Assignment 03 Responses

## Part 4: BigQuery External Tables

### Hourly Observations — CSV External Table SQL

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_csv`
OPTIONS (
  format = 'CSV',
  skip_leading_rows = 1,
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/*.csv']
);
```

### Hourly Observations — JSON-L External Table SQL

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_jsonl`
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/*.jsonl']
);
```

### Hourly Observations — Parquet External Table SQL

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_parquet`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/*.parquet']
);

```

### Site Locations — CSV External Table SQL

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.site_locations_csv`
OPTIONS (
  format = 'CSV',
  skip_leading_rows = 1,
  uris = ['gs://sihanyu_musa_5090/air_quality/sites/site_locations.csv']
);e
```

### Site Locations — JSON-L External Table SQL

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.site_locations_jsonl`
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['gs://sihanyu_musa_5090/air_quality/sites/site_locations.jsonl']
);
```

### Site Locations — GeoParquet External Table SQL

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.site_locations_geoparquet`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://sihanyu_musa_5090/air_quality/sites/site_locations.geoparquet']
);
```

### Cross-Table Join Query

```sql
SELECT
  s.StateAbbreviation AS state,
  AVG(h.value) AS avg_pm25
FROM air_quality.hourly_observations_csv h
JOIN air_quality.site_locations_csv s
ON h.aqsid = s.AQSID
WHERE h.parameter_name = 'PM2.5'
AND h.valid_date = PARSE_DATE('%m/%d/%y', '07/15/24')
GROUP BY state
ORDER BY avg_pm25 DESC;
```

---

## Part 5: Hive-Partitioned External Tables

### Hourly Observations — CSV (hive-partitioned)

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_csv_hive`
WITH PARTITION COLUMNS
OPTIONS (
  format = 'CSV',
  skip_leading_rows = 1,
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/csv/*'],
  hive_partition_uri_prefix = 'gs://sihanyu_musa_5090/air_quality/hourly/csv'
);
```

### Hourly Observations — JSON-L (hive-partitioned)

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_jsonl_hive`
WITH PARTITION COLUMNS
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/jsonl/*'],
  hive_partition_uri_prefix = 'gs://sihanyu_musa_5090/air_quality/hourly/jsonl'
);
```

### Hourly Observations — Parquet (hive-partitioned)

```sql
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_parquet_hive`
WITH PARTITION COLUMNS
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/parquet/*'],
  hive_partition_uri_prefix = 'gs://sihanyu_musa_5090/air_quality/hourly/parquet'
);
```

---

## Part 6: Analysis & Reflection

### 1. File Sizes

**Hourly data (single day):**

| Format  | File Size |
|---------|-----------|
| CSV     |   18M        |
| JSON-L  |   42M        |
| Parquet |   797K        |

**Site locations:**

| Format     | File Size |
|------------|-----------|
| CSV        |   1.0M        |
| JSON-L     |   2.9M        |
| GeoParquet |   476k        |

**Analysis:**
> JSON-L is the largest format, while GeoParquet/Parquet is the smallest. JSON-L repeats field names on every row, making it highly redundant. CSV avoids this by using a single header row, resulting in a more compact file. Parquet uses binary columnar storage with built-in compression, which dramatically reduces file size, which makes it the smallest format for the hourly data. Similarly, GeoParquet is the smallest for site locations, as it encodes geometry efficiently in binary rather than as plain text coordinates.

### 2. Format Anatomy

> CSV is a plain text format with one header row and one record per line, with field values separated by "|" in this case. It is human-readable and can be opened in any text editor. 
Parquet is a binary columnar storage format that data from the same column is stored together rather than row by row. It is not human-readable, but it embeds the schema (field names and data types) directly in the file, and achieves much better compression than CSV.

### 3. Choosing Formats for BigQuery

> Parquet is preferred because BigQuery charges based on the amount of data scanned. Since Parquet uses columnar storage and built-in compression, files are much smaller than CSV or JSON-L, which directly reduces query cost. As for the performance, the BigQuery engine is also columnr, so it can read the columns needed for a query rather than scanning the entire record as for CSV or JSON-L.

### 4. Pipeline vs. Warehouse Joins

> Keeping them as separate tables is more flexible. If needed, the hourly data and site locations can each be queried independently or joined. It also reduces storage since site metadata is not duplicated across every observation row. However, any query that requires location information must perform a join each time, which adds computation overhead. Joining during the prepare step (denormalization) makes queries faster and simpler since coordinates are already embedded in each row, but it significantly increases file size due to repeated site metadata. It also means that if site information changes, the entire prepare step must be re-run to reflect the update.

#### Stretch Challenge (optional)

If you implemented the stretch challenge (scripts `06_prepare`, `06_upload_to_gcs`, `06_create_tables.sql`), paste your SQL statements here:

```sql
-- Merged Hourly + Sites — CSV (hive-partitioned)
```

```sql
-- Merged Hourly + Sites — JSON-L (hive-partitioned)
```

```sql
-- Merged Hourly + Sites — GeoParquet (hive-partitioned)
```

### 5. Choosing a Data Source

For each person below, which air quality data source (AirNow hourly files, AirNow API, AQS bulk downloads, or AQS API) would you recommend, and why?

**a) A parent who wants a dashboard showing current air quality near their child's school:**
> [Your answer here]

**b) An environmental justice advocate identifying neighborhoods with chronically poor air quality over the past decade:**
> [Your answer here]

**c) A school administrator who needs automated morning alerts when AQI exceeds a threshold:**
> [Your answer here]
