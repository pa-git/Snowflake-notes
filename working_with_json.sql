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

Query the data
--------------------------------------------------------------------------
-- It's very important to understand the structure of the json data
-- See json_sample.json file to understand the structure

-- Select the id of the first element in "feeds"         
-- NB: Property names are case sensitive

SELECT
  JSON_DATA:feeds[0].id::NUMBER,
  JSON_DATA:feeds[0].location::STRING,
  JSON_DATA:feeds[0].profilePicture::STRING,
  JSON_DATA:feeds[0].multiMedia[0].url::STRING
FROM MY_JSON_TABLE;
+-------------------------------+-----------------------------------------+-------------------------------------------------+----------------------------------------------+
| JSON_DATA:FEEDS[0].ID::NUMBER | JSON_DATA:FEEDS[0].LOCATION::STRING     | JSON_DATA:FEEDS[0].PROFILEPICTURE::STRING       | JSON_DATA:FEEDS[0].MULTIMEDIA[0].URL::STRING |
|-------------------------------+-----------------------------------------+-------------------------------------------------+----------------------------------------------|
|                          2140 | Hermannplatz 5-6, 10967 Berlin, Germany | Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png | http://www.youtube.com/embed/mPhboJR0Llc     |
+-------------------------------+-----------------------------------------+-------------------------------------------------+----------------------------------------------+
1 Row(s) produced. Time Elapsed: 1.149s

-- This only allows to query one element at a time using its position
-- Use the FLATTEN function to convert JSON data into a tabular view

CREATE OR REPLACE TABLE MY_JSON_TABLE_FLAT AS
SELECT
   a0.VALUE:id::NUMBER as ID,
   a0.VALUE:location::STRING as LOCATION,
   a0.VALUE:profilePicture::STRING as PICTURE,
   a1.VALUE:url::STRING as URL
FROM
   MY_JSON_TABLE
   , LATERAL FLATTEN ( INPUT => JSON_DATA:feeds ) as a0
   , LATERAL FLATTEN ( INPUT => a0.VALUE:multiMedia) as a1;
+------------------------------------------------+
| status                                         |
|------------------------------------------------|
| Table MY_JSON_TABLE_FLAT successfully created. |
+------------------------------------------------+
1 Row(s) produced. Time Elapsed: 2.957s

-- Now you can query the data normally
SELECT * FROM MY_JSON_TABLE_FLAT LIMIT 5;
+------+--------------------------------------------------------------------------------+-------------------------------------------------+---------------------------------------------+
|   ID | LOCATION                                                                       | PICTURE                                         | URL                                         |
|------+--------------------------------------------------------------------------------+-------------------------------------------------+---------------------------------------------|
| 2140 | Hermannplatz 5-6, 10967 Berlin, Germany                                        | Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png | http://www.youtube.com/embed/mPhboJR0Llc    |
| 2139 | 443 N Rodeo Dr, Beverly Hills, CA 90210, USA                                   | Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png | http://www.youtube.com/embed/RtFcZ6Bwolw    |
| 2138 | IFFCO Chowk Flyover, Heritage City, Sector 29, Gurugram, Haryana 122001, India | Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png | http://www.youtube.com/embed/TUT2-FEPMdc    |
| 2137 | 2001 NV-582, Las Vegas, NV 89101, USA                                          | Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png | https://www.youtube.com/watch?v=Kg8VraUgpR4 |
| 2136 | 103 B100, Anglesea VIC 3230, Australia                                         | Images/9b291404-bc2e-4806-88c5-08d29e65a5ad.png | https://www.youtube.com/watch?v=WgmgSwkTUEM |
+------+--------------------------------------------------------------------------------+-------------------------------------------------+---------------------------------------------+
5 Row(s) produced. Time Elapsed: 0.573s

