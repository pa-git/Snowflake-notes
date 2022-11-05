-- Create target table
--------------------------------------------------------------------------
-- You only need a single column of data type VARIANT

CREATE OR REPLACE TABLE MY_JSON_TABLE (
  JSON_DATA VARIANT
);

+-------------------------------------------+
| status                                    |
|-------------------------------------------|
| Table MY_JSON_TABLE successfully created. |
+-------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.316s

-- Put the file. This time I'll just use the table stage
-- NB: the table stage is created by default
--------------------------------------------------------------------------

PUT file://C:\Users\Public\Downloads\json_sample.json @%MY_JSON_TABLE;
+------------------+---------------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source           | target              | source_size | target_size | source_compression | target_compression | status   | message |
|------------------+---------------------+-------------+-------------+--------------------+--------------------+----------+---------|
| json_sample.json | json_sample.json.gz |      339632 |       41072 | NONE               | GZIP               | UPLOADED |         |
+------------------+---------------------+-------------+-------------+--------------------+--------------------+----------+---------+
1 Row(s) produced. Time Elapsed: 0.823s

LIST @%MY_JSON_TABLE;
+---------------------+-------+----------------------------------+------------------------------+
| name                |  size | md5                              | last_modified                |
|---------------------+-------+----------------------------------+------------------------------|
| json_sample.json.gz | 41072 | 0bd41d47d3f2199fe05774717d60b429 | Sat, 5 Nov 2022 16:10:03 GMT |
+---------------------+-------+----------------------------------+------------------------------+
1 Row(s) produced. Time Elapsed: 0.188s

-- Load the data into the table
-- NB: A file format cannot be specified on a table stage
--     Therefore the file format is specified at COPY INTO
--------------------------------------------------------------------------
COPY INTO MY_JSON_TABLE
FROM @%MY_JSON_TABLE
FILE_FORMAT = ( TYPE = 'JSON' );
+---------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
| file                | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
|---------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
| json_sample.json.gz | LOADED |           1 |           1 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
+---------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
1 Row(s) produced. Time Elapsed: 2.191s
