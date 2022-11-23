-- List the files in my user stage
LIST @~;
+----------------+-------+----------------------------------+-------------------------------+
| name           |  size | md5                              | last_modified                 |
|----------------+-------+----------------------------------+-------------------------------|
| titanic.csv.gz | 21584 | 80d5451a5123af21cedeedfd159bdc1a | Tue, 25 Oct 2022 14:15:47 GMT |
+----------------+-------+----------------------------------+-------------------------------+

-- Try to upload the same file again
PUT file://C:\Users\Public\Downloads\titanic.csv @~;
+-------------+----------------+-------------+-------------+--------------------+--------------------+---------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status  | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+---------+---------|
| titanic.csv | titanic.csv.gz |       60302 |           0 | NONE               | GZIP               | SKIPPED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+---------+---------+
1 Row(s) produced. Time Elapsed: 0.815s

-- Note: The file is skipped and is not uploaded

-- Change the content of the file completely and try to upload again
PUT file://C:\Users\Public\Downloads\titanic.csv @~;
+-------------+----------------+-------------+-------------+--------------------+--------------------+---------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status  | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+---------+---------|
| titanic.csv | titanic.csv.gz |       49558 |           0 | NONE               | GZIP               | SKIPPED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+---------+---------+
1 Row(s) produced. Time Elapsed: 1.321s

-- Note: The file is skipped and is not uploaded - Even if the content and size of the file are completely different

-- Avoid that issue by adding OVERWRITE = TRUE to force the upload
PUT file://C:\Users\Public\Downloads\titanic.csv @~ OVERWRITE = TRUE;
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status   | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------|
| titanic.csv | titanic.csv.gz |       49558 |       18000 | NONE               | GZIP               | UPLOADED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
