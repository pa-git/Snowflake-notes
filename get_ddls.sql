CREATE OR REPLACE PROCEDURE GENERATE_DDL(FULL_TABLE_NAME_LIST STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    var tables = FULL_TABLE_NAME_LIST.split(",");
    var ddl_statements = "";
    
    for (var i = 0; i < tables.length; i++) {
        var stmt = snowflake.createStatement({sqlText: `SELECT GET_DDL('table', '` + tables[i] + `')`});
        var res = stmt.execute();
        res.next();
        var ddl = res.getColumnValue(1);
        ddl_statements += ddl + ";\n\n";
    }
    return ddl_statements;
$$;
