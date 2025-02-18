SELECT 
  TO_DATE(load_time) AS load_date,
  SUM(file_size) / (1024*1024) AS mb_loaded
FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY
WHERE load_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY load_date
ORDER BY load_date;


SELECT 
  DATE_TRUNC('day', start_time) AS load_date,
  SUM(file_size) / (1024*1024) AS mb_loaded
FROM TABLE(
  information_schema.copy_history(
    table_name => 'YOUR_TABLE_NAME',
    start_time => DATEADD(day, -30, CURRENT_TIMESTAMP())
  )
)
GROUP BY load_date
ORDER BY load_date;
