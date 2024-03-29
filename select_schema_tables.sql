SELECT
    t.TABLE_SCHEMA as schema,
    t.TABLE_NAME as table,
    kcu.COLUMN_NAME as primary_key
FROM
    INFORMATION_SCHEMA.TABLES t
LEFT JOIN
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
ON
    t.TABLE_SCHEMA = tc.TABLE_SCHEMA
    AND t.TABLE_NAME = tc.TABLE_NAME
    AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
LEFT JOIN
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
ON
    tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
    AND tc.TABLE_NAME = kcu.TABLE_NAME
    AND tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
WHERE
    t.TABLE_SCHEMA = '<YourSchemaName>' -- Replace with your actual schema name
    AND t.TABLE_TYPE = 'BASE TABLE'
ORDER BY
    t.TABLE_NAME;
