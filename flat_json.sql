SELECT
    f.value:column_name::STRING as column_name,
    f.value:has_duplicates_test.Actual::BOOLEAN as has_duplicates_actual,
    f.value:has_duplicates_test.Expected::BOOLEAN as has_duplicates_expected,
    f.value:has_duplicates_test.Message::STRING as has_duplicates_message,
    f.value:null_values_percentage_test.Actual::NUMBER as null_values_actual,
    f.value:null_values_percentage_test.Expected::NUMBER as null_values_expected,
    f.value:null_values_percentage_test.Message::STRING as null_values_message,
    f.value:sum_total_test.Message::STRING as sum_total_message,
    r.value:Actual::NUMBER as row_count_actual,
    r.value:Expected::NUMBER as row_count_expected,
    r.value:Message::STRING as row_count_message,
    r.value:run_version_id::STRING as run_version_id,
    r.value:table_name::STRING as table_name,
    r.value:table_schema::STRING as table_schema,
    r.value:task_name::STRING as task_name,
    r.value:timestamp::TIMESTAMP as timestamp
FROM your_table,
    LATERAL FLATTEN(input => json_data:columns) f,
    LATERAL FLATTEN(input => json_data:row_count_test) r
WHERE f.value IS NOT NULL AND r.value IS NOT NULL;


SELECT
    f.value:column_name::STRING as column_name
FROM your_table,
    LATERAL FLATTEN(input => json_data:columns) f
WHERE 
    f.value:has_duplicates_test.Message::STRING = 'Test Failed'
    OR f.value:null_values_percentage_test.Message::STRING = 'Test Failed'
    OR f.value:sum_total_test.Message::STRING = 'Test Failed';
