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
