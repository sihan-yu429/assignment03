-- Part 4: Create BigQuery external tables
--
-- Create these tables in a dataset named `air_quality`.
-- Use wildcard URIs for the hourly data tables so a single table
-- spans all 31 days of files.
--
-- After creating the tables, verify they work by running:
--     SELECT count(*) FROM air_quality.<table_name>;


-- Hourly Observations — CSV
-- TODO: Create external table `hourly_observations_csv`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.csv


-- Hourly Observations — JSON-L
-- TODO: Create external table `hourly_observations_jsonl`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.jsonl


-- Hourly Observations — Parquet
-- TODO: Create external table `hourly_observations_parquet`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.parquet


-- Site Locations — CSV
-- TODO: Create external table `site_locations_csv`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.csv


-- Site Locations — JSON-L
-- TODO: Create external table `site_locations_jsonl`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.jsonl


-- Site Locations — GeoParquet
-- TODO: Create external table `site_locations_geoparquet`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.geoparquet


-- Cross-table join query
-- Write a query that joins hourly observations with site locations
-- to get latitude/longitude for each observation. For example,
-- find the average PM2.5 value by state for a single day.



-- Hourly Observations — CSV
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_csv`
OPTIONS (
  format = 'CSV',
  skip_leading_rows = 1,
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/*.csv']
);

-- Hourly Observations — JSON-L
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_jsonl`
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/*.jsonl']
);

-- Hourly Observations — Parquet
CREATE OR REPLACE EXTERNAL TABLE `air_quality.hourly_observations_parquet`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://sihanyu_musa_5090/air_quality/hourly/*.parquet']
);

-- Site Locations — CSV
CREATE OR REPLACE EXTERNAL TABLE `air_quality.site_locations_csv`
OPTIONS (
  format = 'CSV',
  skip_leading_rows = 1,
  uris = ['gs://sihanyu_musa_5090/air_quality/sites/site_locations.csv']
);

-- Site Locations — JSON-L
CREATE OR REPLACE EXTERNAL TABLE `air_quality.site_locations_jsonl`
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['gs://sihanyu_musa_5090/air_quality/sites/site_locations.jsonl']
);

-- Site Locations — GeoParquet
CREATE OR REPLACE EXTERNAL TABLE `air_quality.site_locations_geoparquet`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://sihanyu_musa_5090/air_quality/sites/site_locations.geoparquet']
);

SELECT count(*) FROM air_quality.hourly_observations_csv;
SELECT count(*) FROM air_quality.hourly_observations_jsonl;
SELECT count(*) FROM air_quality.hourly_observations_parquet;
SELECT count(*) FROM air_quality.site_locations_csv;
SELECT count(*) FROM air_quality.site_locations_jsonl;
SELECT count(*) FROM air_quality.site_locations_geoparquet;


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