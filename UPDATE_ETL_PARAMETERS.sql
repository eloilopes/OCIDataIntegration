create or replace PROCEDURE "UPDATE_ETL_PARAMETERS" 
(TABLE_NAME IN VARCHAR2, TASK_RUN_KEY IN VARCHAR2,
STATUS IN VARCHAR2, CODE IN VARCHAR2, TABLE_OUT OUT VARCHAR2, CODE_OUT OUT VARCHAR2 ) 
is
begin
EXECUTE IMMEDIATE 'insert into MANAGE_ETL (SOURCE,TABLE_NAME, task_key, STATUS, CODE) values (' || '''' || 'ADW' ||''',' || '''' || TABLE_NAME || ''''
|| ' , ' || '''' || task_run_key || '''' || ' , ' || '''' || STATUS || '''' 
|| ' , ' || '''' || CODE || '''' || ' ) ';
SELECT TABLE_NAME, CODE into TABLE_OUT, CODE_OUT from dual;

END UPDATE_ETL_PARAMETERS;
