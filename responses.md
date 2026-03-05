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
| CSV     |           |
| JSON-L  |           |
| Parquet |           |

**Site locations:**

| Format     | File Size |
|------------|-----------|
| CSV        |           |
| JSON-L     |           |
| GeoParquet |           |

**Analysis:**
> [Your answer here — which is smallest/largest and why?]

### 2. Format Anatomy

> [Pick two formats and describe their structure. What are the key differences?]

### 3. Choosing Formats for BigQuery

> [Why is Parquet preferred over CSV or JSON-L? Consider performance and cost.]

### 4. Pipeline vs. Warehouse Joins

> [You kept hourly data and site locations as separate tables and joined them in BigQuery. What if you had joined them during the prepare step instead (denormalization)? What are the trade-offs of each approach?]

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
