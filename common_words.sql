-- SQL Query to find the most frequent words in column names

WITH ColumnWords AS (
    SELECT 
        -- Split the column name into words using underscore as a delimiter
        SPLIT_PART(columns.COLUMN_NAME, '_', seq4()) AS Word
    FROM 
        INFORMATION_SCHEMA.COLUMNS,
        TABLE(GENERATOR(ROWCOUNT => 100)) -- Generate a series of numbers for splitting
    WHERE 
        columns.TABLE_SCHEMA = '<Your_Schema>' AND 
        columns.TABLE_NAME = '<Your_Table>' AND
        seq4() <= REGEXP_COUNT(columns.COLUMN_NAME, '_') + 1 -- Ensure splitting at each underscore
)
SELECT 
    Word, 
    COUNT(*) AS Frequency
FROM 
    ColumnWords
GROUP BY 
    Word
ORDER BY 
    Frequency DESC, Word;
