+-----------------------------------------------------+
| Getting started                                     |
|-----------------------------------------------------|
| 1- Access your account using SnowSQL                |
| 2- Create a database                                |
| 3- Create a table                                   |
| 4- Create a vitual warehouse                        |
| 5- Load data using User, Table and Named Stage      |
| 6- Create a File Format and a Named Stage           |
+-----------------------------------------------------+

-- Access your account;
----------------------------------------
-- First you need a Snowflake account: https://signup.snowflake.com/
-- Second you will have installed SnowSQL: https://docs.snowflake.com/en/user-guide/snowsql-install-config.html
-- Then in your Terminal:

λ snowsql -a XXXXXXX.canada-central.azure -u PACO
Password:

* SnowSQL * v1.2.23
Type SQL statements or !help

-- Create a database;
----------------------------------------

CREATE OR REPLACE DATABASE SANDBOX;
+----------------------------------------+
| status                                 |
|----------------------------------------|
| Database SANDBOX successfully created. |
+----------------------------------------+
1 Row(s) produced. Time Elapsed: 0.214s

-- Public schema is created by default;
PACO#(no warehouse)@SANDBOX.PUBLIC>SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();
+--------------------+------------------+
| CURRENT_DATABASE() | CURRENT_SCHEMA() |
|--------------------+------------------|
| SANDBOX            | PUBLIC           |
+--------------------+------------------+
1 Row(s) produced. Time Elapsed: 0.129s

-- Create a table;
----------------------------------------
-- See Snowflake datatypes: https://docs.snowflake.com/en/sql-reference/data-types.html;
-- I mostlhy use NUMBER for anything NUMERIC, VARCHAR for any TEXT, VARIANT for semi structured data such as JSON;

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

-- Create a vitual warehouse;
----------------------------------------
-- A Virtual Warehouse is needed to load data and run queries;

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

----------------------------------------
-- Loading data is a 2 step process: PUT (Upload file to stage) and COPY (into table);
-- There are 3 possible stages: User, Table and Named stage;
-- User stage and table stage are created by default;
-- Named stage are managed by the user;
----------------------------------------

-- Example: Load data using user stage;
----------------------------------------

PACO#SANDBOX_WH@SANDBOX.PUBLIC>PUT file://C:\Users\Public\Downloads\titanic.csv @~;
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status   | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------|
| titanic.csv | titanic.csv.gz |       60302 |       21584 | NONE               | GZIP               | UPLOADED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
1 Row(s) produced. Time Elapsed: 1.028s

PACO#SANDBOX_WH@SANDBOX.PUBLIC>COPY INTO TITANIC FROM @~/titanic.csv
                               FILE_FORMAT = (TYPE = csv FIELD_DELIMITER = "," FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
+----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
| file           | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
|----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
| titanic.csv.gz | LOADED |         891 |         891 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
+----------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
1 Row(s) produced. Time Elapsed: 2.034s

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

-- Example: Load using table stage;
----------------------------------------

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

-- Truncate and do it again from Named Stage;
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

-- Example: Load data using named stage;
----------------------------------------

-- Create a file format;
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

-- Create the named stage with this file format;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>CREATE STAGE MY_CSV_STAGE FILE_FORMAT = MYCSVFORMAT;
+-----------------------------------------------+
| status                                        |
|-----------------------------------------------|
| Stage area MY_CSV_STAGE successfully created. |
+-----------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.230s

-- List the named stages;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>SHOW STAGES;
+-------------------------------+--------------+---------------+-------------+-----+-----------------+--------------------+--------------+---------+--------+----------+-------+----------------------+---------------------+
| created_on                    | name         | database_name | schema_name | url | has_credentials | has_encryption_key | owner        | comment | region | type     | cloud | notification_channel | storage_integration |
|-------------------------------+--------------+---------------+-------------+-----+-----------------+--------------------+--------------+---------+--------+----------+-------+----------------------+---------------------|
| 2022-10-25 07:38:36.896 -0700 | MY_CSV_STAGE | SANDBOX       | PUBLIC      |     | N               | N                  | ACCOUNTADMIN |         | NULL   | INTERNAL | NULL  | NULL                 | NULL                |
+-------------------------------+--------------+---------------+-------------+-----+-----------------+--------------------+--------------+---------+--------+----------+-------+----------------------+---------------------+
1 Row(s) produced. Time Elapsed: 0.146s

-- Put the file in my_csv_stage;
PACO#SANDBOX_WH@SANDBOX.PUBLIC>PUT file://C:\Users\Public\Downloads\titanic.csv @MY_CSV_STAGE AUTO_COMPRESS = TRUE;
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
| source      | target         | source_size | target_size | source_compression | target_compression | status   | message |
|-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------|
| titanic.csv | titanic.csv.gz |       60302 |       21584 | NONE               | GZIP               | UPLOADED |         |
+-------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------+
1 Row(s) produced. Time Elapsed: 1.455s

-- Copy into the table;
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
