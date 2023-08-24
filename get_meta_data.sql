INSERT INTO your_desired_table_name (table_name, column_name, data_type, size, sample_value_1, sample_value_2, sample_value_3)
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH AS size,
    ARRAY_SLICE(ARRAY_AGG(VALUE::STRING), 0, 2)[0] AS sample_value_1,
    ARRAY_SLICE(ARRAY_AGG(VALUE::STRING), 0, 2)[1] AS sample_value_2,
    ARRAY_SLICE(ARRAY_AGG(VALUE::STRING), 0, 2)[2] AS sample_value_3
FROM INFORMATION_SCHEMA.COLUMNS 
LEFT JOIN (
    SELECT * FROM the_source_table_name
    LIMIT 100  -- Increase if necessary, this is to limit the number of rows for sampling
) AS samples
ON TRUE
WHERE TABLE_NAME = 'the_source_table_name'
GROUP BY TABLE_NAME, COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH;
