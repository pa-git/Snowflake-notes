-- First let's preview the data

SELECT * FROM TITANIC LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 0.849s

-- Now let's do something bad

UPDATE TITANIC SET PASSENGERID = 0;
+------------------------+-------------------------------------+
| number of rows updated | number of multi-joined rows updated |
|------------------------+-------------------------------------|
|                    891 |                                   0 |
+------------------------+-------------------------------------+
891 Row(s) produced. Time Elapsed: 1.848s

-- Time travel
----------------------------------------------------
-- Some time in the future, we query the data and see that all the Passenger ID are 0 !

SELECT * FROM TITANIC LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           0 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           0 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           0 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           0 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           0 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 0.531s

-- First let's find the statement that changed our data in the query history
SELECT
   START_TIME,
   END_TIME,
   QUERY_ID,
   QUERY_TEXT,
   QUERY_TYPE
FROM
   TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE
   DATABASE_NAME = 'SANDBOX' AND
   SCHEMA_NAME = 'PUBLIC' AND
   QUERY_TYPE = 'UPDATE'
ORDER BY START_TIME DESC;
+-------------------------------+-------------------------------+--------------------------------------+-------------------------------------+------------+
| START_TIME                    | END_TIME                      | QUERY_ID                             | QUERY_TEXT                          | QUERY_TYPE |
|-------------------------------+-------------------------------+--------------------------------------+-------------------------------------+------------|
| 2022-11-06 04:25:34.834 -0800 | 2022-11-06 04:25:36.617 -0800 | 01a820a9-0000-7442-0001-83ba0002a05e | UPDATE TITANIC SET PASSENGERID = 0; | UPDATE     |
+-------------------------------+-------------------------------+--------------------------------------+-------------------------------------+------------+
1 Row(s) produced. Time Elapsed: 0.796s

-- See what the data looked like when this query was run (Using the START_TIME)
SELECT * FROM TITANIC
AT ( TIMESTAMP => '2022-11-06 04:25:34.834 -0800'::timestampltz )
LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 0.605s

-- Or using the query id
SELECT * FROM TITANIC
BEFORE ( STATEMENT => '01a820a9-0000-7442-0001-83ba0002a05e' )
LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 1.047s


-- See what the data looked like after this query was run (Using the END_TIME)
SELECT * FROM TITANIC
 AT ( TIMESTAMP => '2022-11-06 04:25:36.617 -0800'::timestampltz )
 LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           0 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           0 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           0 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           0 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           0 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 0.368s

-- Or using the query ID
SELECT * FROM TITANIC
AT ( STATEMENT => '01a820a9-0000-7442-0001-83ba0002a05e' )
LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           0 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           0 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           0 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           0 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           0 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 0.361s

-- See what the data looked like 30 minutes ago
SELECT * FROM TITANIC
 AT ( OFFSET => -60*30 )
 LIMIT 5;
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
| PASSENGERID | SURVIVED | PCLASS | NAME                                                | SEX    | AGE | SIBSP | PARCH | TICKET           |     FARE | CABIN | EMBARKED |
|-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------|
|           1 |        0 |      3 | Braund, Mr. Owen Harris                             | male   |  22 |     1 |     0 | A/5 21171        |  7.25000 | NULL  | S        |
|           2 |        1 |      1 | Cumings, Mrs. John Bradley (Florence Briggs Thayer) | female |  38 |     1 |     0 | PC 17599         | 71.28330 | C85   | C        |
|           3 |        1 |      3 | Heikkinen, Miss. Laina                              | female |  26 |     0 |     0 | STON/O2. 3101282 |  7.92500 | NULL  | S        |
|           4 |        1 |      1 | Futrelle, Mrs. Jacques Heath (Lily May Peel)        | female |  35 |     1 |     0 | 113803           | 53.10000 | C123  | S        |
|           5 |        0 |      3 | Allen, Mr. William Henry                            | male   |  35 |     0 |     0 | 373450           |  8.05000 | NULL  | S        |
+-------------+----------+--------+-----------------------------------------------------+--------+-----+-------+-------+------------------+----------+-------+----------+
5 Row(s) produced. Time Elapsed: 0.267s


