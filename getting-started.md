# Connect to Snowflake using SnowSQL CLI
λ snowsql -a XXXXXXX.canada-central.azure -u PACO
Password:

* SnowSQL * v1.2.23
Type SQL statements or !help

PACO#(no warehouse)@(no database).(no schema)>-- Create a database
PACO#(no warehouse)@(no database).(no schema)>CREATE OR REPLACE DATABASE SANDBOX;
+----------------------------------------+
| status                                 |
|----------------------------------------|
| Database SANDBOX successfully created. |
+----------------------------------------+
1 Row(s) produced. Time Elapsed: 0.214s

PACO#(no warehouse)@SANDBOX.PUBLIC>-- Public schema is created by default;
PACO#(no warehouse)@SANDBOX.PUBLIC>SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();
+--------------------+------------------+
| CURRENT_DATABASE() | CURRENT_SCHEMA() |
|--------------------+------------------|
| SANDBOX            | PUBLIC           |
+--------------------+------------------+
1 Row(s) produced. Time Elapsed: 0.129s
PACO#(no warehouse)@SANDBOX.PUBLIC>-- Create a table;
-- Create a table;
PACO#(no warehouse)@SANDBOX.PUBLIC>CREATE OR REPLACE TABLE TITANIC (
                                   PassengerId NUMBER,
                                   Survived NUMBER,
                                   Pclass NUMBER,
                                   Name VARCHAR,
                                   Sex VARCHAR,
                                   Age NUMBER,
                                   SibSp NUMBER,
                                   Parch NUMBER,
                                   Ticket VARCHAR,
                                   Fare NUMBER(38,5),
                                   Cabin VARCHAR,
                                   Embarked VARCHAR
                                   );
+-------------------------------------+
| status                              |
|-------------------------------------|
| Table TITANIC successfully created. |
+-------------------------------------+
1 Row(s) produced. Time Elapsed: 0.850s
PACO#(no warehouse)@SANDBOX.PUBLIC>-- See Snowflake datatypes: https://docs.snowflake.com/en/sql-reference/data-types.html;
-- See Snowflake datatypes: https://docs.snowflake.com/en/sql-reference/data-types.html;
PACO#(no warehouse)@SANDBOX.PUBLIC>-- I mostlhy use NUMBER for anything NUMERIC, VARCHAR for any TEXT, VARIANT for semi structu
                                   red data such as JSON;
-- I mostlhy use NUMBER for anything NUMERIC, VARCHAR for any TEXT, VARIANT for semi structured data such as JSON;
PACO#(no warehouse)@SANDBOX.PUBLIC>-- A Virtual Warehouse is need to load data and run queries;
-- A Virtual Warehouse is need to load data and run queries;
PACO#(no warehouse)@SANDBOX.PUBLIC>CREATE OR REPLACE WAREHOUSE SANDBOX_WH WITH
                                   WAREHOUSE_SIZE = 'X-SMALL'
                                   AUTO_SUSPEND = 180
                                   AUTO_RESUME = TRUE
                                   INITIALLY_SUSPENDED = TRUE;
+--------------------------------------------+
| status                                     |
|--------------------------------------------|
| Warehouse SANDBOX_WH successfully created. |
+--------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.618s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Loading data is a 2 step process: Stage and Copy;
-- Loading data is a 2 step process: Stage and Copy;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- There are 3 possible stages: User, Table and Named stage;

-- There are 3 possible stages: User, Table and Named stage;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- User stage and table stage are created by default;
-- User stage and table stage are created by default;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Load using user stage example;
-- Load using user stage example;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>PUT FILE://C:\Users\Public\Downloads\titanic.csv @~;
001003 (42000): SQL compilation error:
syntax error line 1 at position 4 unexpected 'FILE'.
PACO#SANDBOX_WH@SANDBOX.PUBLIC>PUT file://C:\Users\Public\Downloads\titanic.csv @~;
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status   | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------|
| titanic.csv | titanic.csv.gz |       60302 |       21584 | NONE               | GZIP               | UPLOADED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
1 Row(s) produced. Time Elapsed: 1.028s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC FROM @~/titanic.csv;
100016 (22000): Field delimiter ',' found while expecting record delimiter '\n'
  File '@~/titanic.csv.gz', line 2, character 60
  Row 2, column "TITANIC"["EMBARKED":12]
  If you would like to continue loading when an error is encountered, use other values such as 'SKIP_FILE' or 'CONTINUE' for the ON_ERROR option. For more information on loading options, please run 'info loading_data' in a SQL client.
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC FROM @~/titanic.csv ;
100016 (22000): Field delimiter ',' found while expecting record delimiter '\n'
  File '@~/titanic.csv.gz', line 2, character 60
  Row 2, column "TITANIC"["EMBARKED":12]
  If you would like to continue loading when an error is encountered, use other values such as 'SKIP_FILE' or 'CONTINUE' for the ON_ERROR option. For more information on loading options, please run 'info loading_data' in a SQL client.
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC FROM @~/titanic.csv
                               FILE_FORMAT = (Exception in thread Thread-1212:
Traceback (most recent call last):
  File "snowflake\cli\parseutils.py", line 100, in extract_from_part
StopIteration

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "threading.py", line 932, in _bootstrap_inner
  File "threading.py", line 870, in run
  File "prompt_toolkit\interface.py", line 865, in run
  File "snowflake\cli\sqlcompleter.py", line 303, in get_completions
  File "snowflake\cli\completion_engine.py", line 91, in suggest_type
  File "snowflake\cli\completion_engine.py", line 218, in suggest_based_on_last_token

  File "snowflake\cli\parseutils.py", line 176, in extract_tables
  File "snowflake\cli\parseutils.py", line 143, in extract_table_identifiers
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC FROM @~/titanic.csv
                               FILE_FORMAT = (
                               ;
001003 (42000): SQL compilation error:
syntax error line 3 at position 0 unexpected ';'.
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC FROM @~/titanic.csv
                               FILE_FORMAT = (TYPE = csv FIELD_DELIMITER = "," FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
+----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
| file           | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
|----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
| titanic.csv.gz | LOADED |         891 |         891 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
+----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
1 Row(s) produced. Time Elapsed: 2.034s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Check data;
-- Check data;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>SELECT * FROM TITANIC LIMIT 10;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
|           6 |        0 |      3 | Moran, Mr. James                                    | male   | NULL |     0 |     0 | 330877           |  8.45830 | NULL  | Q        |
|           7 |        0 |      1 | McCarthy, Mr. Timothy J                             | male   |  54 |     0 |     0 | 17463            | 51.86250 | E46   | S        |
|           8 |        0 |      3 | Palsson, Master. Gosta Leonard                      | male   |   2 |     3 |     1 | 349909           | 21.07500 | NULL  | S        |
|           9 |        1 |      3 | Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)   | female |  27 |     0 |     2 | 347742           | 11.13330 | NULL  | S        |
|          10 |        1 |      2 | Nasser, Mrs. Nicholas (Adele Achem)                 | female |  14 |     1 |     0 | 237736           | 30.07080 | NULL  | C        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
10 Row(s) produced. Time Elapsed: 0.773s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Truncate and do it again from Table Stage;
-- Truncate and do it again from Table Stage;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>TRUNCATE TITANIC;
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.676s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>SELECT * FROM TITANIC LIMIT 10;
+-------------+----------+--------+------+-----+-----+-------+-------+--------+------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME | SEX | AGE | SIBSP | PARCH | TICKET | FARE | CABIN | EMBARKED |
|-------------+----------+--------+------+-----+-----+-------+-------+--------+------+-------+----------|
+-------------+----------+--------+------+-----+-----+-------+-------+--------+------+-------+----------+
0 Row(s) produced. Time Elapsed: 0.836s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Load using table stage example;
-- Load using table stage example;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>PUT file://C:\Users\Public\Downloads\titanic.csv @%TITANIC;
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status   | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------|
| titanic.csv | titanic.csv.gz |       60302 |       21584 | NONE               | GZIP               | UPLOADED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
1 Row(s) produced. Time Elapsed: 1.063s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC FROM @%TITANIC/titanic.csv
                               FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = "," FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
+----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
| file           | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
|----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
| titanic.csv.gz | LOADED |         891 |         891 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
+----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
1 Row(s) produced. Time Elapsed: 1.298s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Check data;
-- Check data;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>SELECT * FROM TITANIC LIMIT 10;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
|           6 |        0 |      3 | Moran, Mr. James                                    | male   | NULL |     0 |     0 | 330877           |  8.45830 | NULL  | Q        |
|           7 |        0 |      1 | McCarthy, Mr. Timothy J                             | male   |  54 |     0 |     0 | 17463            | 51.86250 | E46   | S        |
|           8 |        0 |      3 | Palsson, Master. Gosta Leonard                      | male   |   2 |     3 |     1 | 349909           | 21.07500 | NULL  | S        |
|           9 |        1 |      3 | Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)   | female |  27 |     0 |     2 | 347742           | 11.13330 | NULL  | S        |
|          10 |        1 |      2 | Nasser, Mrs. Nicholas (Adele Achem)                 | female |  14 |     1 |     0 | 237736           | 30.07080 | NULL  | C        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
10 Row(s) produced. Time Elapsed: 1.638s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Truncate and do it again from Named Stage;
-- Truncate and do it again from Named Stage;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>TRUNCATE TITANIC:
001003 (42000): SQL compilation error:
syntax error line 1 at position 16 unexpected ':'.
PACO#SANDBOX_WH@SANDBOX.PUBLIC>TRUNCATE TITANIC;
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.369s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>SELECT * FROM TITANIC LIMIT 10;
+-------------+----------+--------+------+-----+-----+-------+-------+--------+------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME | SEX | AGE | SIBSP | PARCH | TICKET | FARE | CABIN | EMBARKED |
|-------------+----------+--------+------+-----+-----+-------+-------+--------+------+-------+----------|
+-------------+----------+--------+------+-----+-----+-------+-------+--------+------+-------+----------+
0 Row(s) produced. Time Elapsed: 0.315s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- First create Named Stage;
-- First create Named Stage;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Create a file format;
-- Create a file format;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>CREATE OR REPLACE FILE FORMAT MYCSVFORMAT
                               TYPE = 'CSV'
                               FIELD_DELIMITER = ','
                               SKIP_HEADER = 1;
+-----------------------------------------------+
| status                                        |
|-----------------------------------------------|
| File format MYCSVFORMAT successfully created. |
+-----------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.580s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Create the named stage with this file format;
-- Create the named stage with this file format;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>CREATE STAGE MY_CSV_STAGE FILE_FORMAT = MYCSVFORMAT;
+-----------------------------------------------+
| status                                        |
|-----------------------------------------------|
| Stage area MY_CSV_STAGE successfully created. |
+-----------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.230s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- List the named stages;
-- List the named stages;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>SHOW STAGES;
+-------------------------------+--------------+---------------+-------------+-----+-----------------+--------------------+--------------+---------+--------+----------+-------+----------------------+---------------------+
| created_on                    | name         | database_name | schema_name | url | has_credentials | has_encryption_key | owner        | comment | region | type     | cloud | notification_channel | storage_integration |
|-------------------------------+--------------+---------------+-------------+-----+-----------------+--------------------+--------------+---------+--------+----------+-------+----------------------+---------------------|
| 2022-10-25 07:38:36.896 -0700 | MY_CSV_STAGE | SANDBOX       | PUBLIC      |     | N               | N                  | ACCOUNTADMIN |         | NULL   | INTERNAL | NULL  | NULL                 | NULL                |
+-------------------------------+--------------+---------------+-------------+-----+-----------------+--------------------+--------------+---------+--------+----------+-------+----------------------+---------------------+
1 Row(s) produced. Time Elapsed: 0.146s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Put the file in my_csv_stage;
-- Put the file in my_csv_stage;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>PUT file://C:\Users\Public\Downloads\titanic.csv @MY_CSV_STAGE AUTO_COMPRESS = TRUE;
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status   | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------|
| titanic.csv | titanic.csv.gz |       60302 |       21584 | NONE               | GZIP               | UPLOADED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
1 Row(s) produced. Time Elapsed: 1.455s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Copy into the table;
-- Copy into the table;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC
                               FROM @MY_CSV_STAGE/titanic.csv
                               FILE_FORMAT = (FORMAT_NAME = MYCSVFORMAT)
                               ON_ERROR = 'SKIP_FILE';
+-----------------------------+-------------+-------------+-------------+-------------+-------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------+-----------------------+-------------------------+
| file                        | status      | rows_parsed | rows_loaded | error_limit | errors_seen | first_error                                                                                                                                                          | first_error_line | first_error_character | first_error_column_name |
|-----------------------------+-------------+-------------+-------------+-------------+-------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------+-----------------------+-------------------------|
| my_csv_stage/titanic.csv.gz | LOAD_FAILED |         891 |           0 |           1 |         891 | Number of columns in file (13) does not match that of the corresponding table (12), use file format option error_on_column_count_mismatch=false to ignore this error |                3 |                     1 | "TITANIC"[13]           |
+-----------------------------+-------------+-------------+-------------+-------------+-------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------+-----------------------+-------------------------+
1 Row(s) produced. Time Elapsed: 2.084s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>CREATE OR REPLACE FILE FORMAT MYCSVFORMAT
                                                              TYPE = 'CSV'
                                                              FIELD_DELIMITER = ','
                                                              SKIP_HEADER = 1;
+-----------------------------------------------+
| status                                        |
|-----------------------------------------------|
| File format MYCSVFORMAT successfully created. |
+-----------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.181s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>CREATE OR REPLACE FILE FORMAT MYCSVFORMAT
                               TYPE = 'CSV'
                               FIELD_DELIMITER = ','
                               SKIP_HEADER = 1;
+-----------------------------------------------+
| status                                        |
|-----------------------------------------------|
| File format MYCSVFORMAT successfully created. |
+-----------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.195s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>CREATE OR REPLACE FILE FORMAT MYCSVFORMAT
                               TYPE = 'CSV'
                               FIELD_DELIMITER = ','
                               FIELD_OPTIONALLY_ENCLOSED_BY = '"'
                               SKIP_HEADER = 1;
+-----------------------------------------------+
| status                                        |
|-----------------------------------------------|
| File format MYCSVFORMAT successfully created. |
+-----------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.178s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC
                               FROM @MY_CSV_STAGE/titanic.csv
                               FILE_FORMAT = (FORMAT_NAME = MYCSVFORMAT)
                               ON_ERROR = 'SKIP_FILE';
+-----------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
| file                        | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
|-----------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
| my_csv_stage/titanic.csv.gz | LOADED |         891 |         891 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
+-----------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
1 Row(s) produced. Time Elapsed: 1.457s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>-- Check data;
-- Check data;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>SELECT * FROM TITANIC LIMIT 10;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
|           6 |        0 |      3 | Moran, Mr. James                                    | male   | NULL |     0 |     0 | 330877           |  8.45830 | NULL  | Q        |
|           7 |        0 |      1 | McCarthy, Mr. Timothy J                             | male   |  54 |     0 |     0 | 17463            | 51.86250 | E46   | S        |
|           8 |        0 |      3 | Palsson, Master. Gosta Leonard                      | male   |   2 |     3 |     1 | 349909           | 21.07500 | NULL  | S        |
|           9 |        1 |      3 | Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)   | female |  27 |     0 |     2 | 347742           | 11.13330 | NULL  | S        |
|          10 |        1 |      2 | Nasser, Mrs. Nicholas (Adele Achem)                 | female |  14 |     1 |     0 | 237736           | 30.07080 | NULL  | C        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
10 Row(s) produced. Time Elapsed: 0.273s
PACO#SANDBOX_WH@SANDBOX.PUBLIC>
