CREATE OR REPLACE PROCEDURE get_sample_values(TABLE_NAME STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
  var columns_query = `SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '${TABLE_NAME}'`;
  var stmt = snowflake.createStatement({sqlText: columns_query});
  var column_result = stmt.execute();

  var column_names = [];
  while (column_result.next()) {
    column_names.push(column_result.getColumnValue(1));
  }

  var sample_queries = column_names.map(function(col) {
    return `ARRAY_AGG(DISTINCT ${col}) WITHIN GROUP (ORDER BY ${col}) AS Sample_${col}`;
  }).join(', ');

  var sample_query = `SELECT ${sample_queries} FROM (SELECT * FROM ${TABLE_NAME} LIMIT 10)`;
  
  var sample_stmt = snowflake.createStatement({sqlText: sample_query});
  var sample_result = sample_stmt.execute();

  var result = {};
  while (sample_result.next()) {
    for (var i = 1; i <= column_names.length; i++) {
      result[column_names[i-1]] = sample_result.getColumnValue(i);
    }
  }

  return JSON.stringify(result);
$$;

CREATE OR REPLACE PROCEDURE get_sample_values_and_types(TABLE_NAME STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
  var columns_query = `SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '${TABLE_NAME}'`;
  var stmt = snowflake.createStatement({sqlText: columns_query});
  var column_result = stmt.execute();

  var column_metadata = [];
  while (column_result.next()) {
    column_metadata.push({
      name: column_result.getColumnValue(1),
      data_type: column_result.getColumnValue(2),
      size: column_result.getColumnValue(3)
    });
  }

  var sample_queries = column_metadata.map(function(col) {
    return `ARRAY_AGG(DISTINCT ${col.name}) WITHIN GROUP (ORDER BY ${col.name}) AS Sample_${col.name}`;
  }).join(', ');

  var sample_query = `SELECT ${sample_queries} FROM (SELECT * FROM ${TABLE_NAME} LIMIT 10)`;
  
  var sample_stmt = snowflake.createStatement({sqlText: sample_query});
  var sample_result = sample_stmt.execute();

  var result = {};
  while (sample_result.next()) {
    for (var i = 0; i < column_metadata.length; i++) {
      result[column_metadata[i].name] = {
        data_type: column_metadata[i].data_type,
        size: column_metadata[i].size,
        sample_values: sample_result.getColumnValue(i+1)
      };
    }
  }

  return JSON.stringify(result);
$$;
