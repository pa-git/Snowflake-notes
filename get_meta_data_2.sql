DECLARE @sql STRING;

SET @sql = (SELECT LISTAGG(
    'SELECT ''' || TABLE_NAME || ''' AS table_name, ''' || COLUMN_NAME || ''' AS column_name, ''' || DATA_TYPE || ''' AS data_type, ' || 
    CASE WHEN DATA_TYPE = 'VARCHAR' THEN CHARACTER_MAXIMUM_LENGTH ELSE 'NULL' END || ' AS size, ' || 
    'ARRAY_SLICE(ARRAY_AGG(' || COLUMN_NAME || '::STRING), 0, 2)[0] AS sample_value_1, ' ||
    'ARRAY_SLICE(ARRAY_AGG(' || COLUMN_NAME || '::STRING), 0, 2)[1] AS sample_value_2, ' ||
    'ARRAY_SLICE(ARRAY_AGG(' || COLUMN_NAME || '::STRING), 0, 2)[2] AS sample_value_3 ' ||
    'FROM the_source_table_name GROUP BY 1,2,3,4'
    , ' UNION ALL ') 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'the_source_table_name');

-- Execute the dynamically generated SQL
EXECUTE IMMEDIATE @sql;
