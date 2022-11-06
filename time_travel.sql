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

-- Let's see what that looks like
-- All the Passenger ID are 0

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

