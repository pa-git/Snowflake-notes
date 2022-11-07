-- Create DB

CREATE OR REPLACE DATABASE SHARING_DEMO;
+---------------------------------------------+
| status                                      |
|---------------------------------------------|
| Database SHARING_DEMO successfully created. |
+---------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.218s

-- Create a table
CREATE OR REPLACE TABLE SHARING_TITANIC AS
SELECT * FROM SANDBOX.PUBLIC.TITANIC;
+---------------------------------------------+
| status                                      |
|---------------------------------------------|
| Table SHARING_TITANIC successfully created. |
+---------------------------------------------+
1 Row(s) produced. Time Elapsed: 2.068s

-- Preview data
SELECT * FROM SHARING_TITANIC LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 0.312s

-- Use role ACCOUNTADMIN to create a share. 
-- ACCOUNTADMIN can also GRANT create share privilege to non-ACCOUNTADMIN
-- Ownership of the SHARE as well as the objects in the share are needed

USE ROLE ACCOUNTADMIN;
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.150s

-- Create the SHARE object
CREATE SHARE SHARE_TITANIC;
+-------------------------------------------+
| status                                    |
|-------------------------------------------|
| Share SHARE_TITANIC successfully created. |
+-------------------------------------------+
1 Row(s) produced. Time Elapsed: 0.711s

-- Grant usage and select to the SHARE
-- Grant the database
GRANT USAGE ON DATABASE SHARING_DEMO TO SHARE SHARE_TITANIC;
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.184s

-- Grant the Schema
GRANT USAGE ON SCHEMA SHARING_DEMO.PUBLIC TO SHARE SHARE_TITANIC;
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.179s

-- Grant the table
GRANT SELECT ON TABLE SHARING_DEMO.PUBLIC.SHARING_TITANIC TO SHARE SHARE_TITANIC;
+----------------------------------+
| status                           |
|----------------------------------|
| Statement executed successfully. |
+----------------------------------+
1 Row(s) produced. Time Elapsed: 0.163s

-- Add the consumer account to the share
ALTER SHARE SHARE_TITANIC ADD ACCOUNT = < CONSUMER_ACCOUNT >

-- The consumer account will now have access to the share
