SELECT id, 
       flattened.value:"$key"::STRING AS variable, 
       flattened.value:"$value"::INT AS value
FROM sample_data,
LATERAL FLATTEN(TO_VARIANT(sample_data)) AS flattened
WHERE flattened.value:"$key" != 'id';
