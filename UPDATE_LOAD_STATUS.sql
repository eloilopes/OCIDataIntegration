create or replace PROCEDURE "UPDATE_LOAD_STATUS" 
(task_run_key IN VARCHAR2,
STATUS IN VARCHAR2,
ERROR_MESSAGE IN VARCHAR2,
NO_OF_INSERTS IN number,
DURATION IN number,START_TIME IN TIMESTAMP, END_TIME IN TIMESTAMP) 
is
getTasks dbms_cloud_oci_di_data_integration_list_task_runs_response_t;
getBody dbms_cloud_oci_dataintegration_task_run_summary_collection_t;
getListTaskSummary dbms_cloud_oci_dataintegration_task_run_summary_tbl;
begin
//The DBMS_CLOUD_OCI_DI_DATA_INTEGRATION.LIST_TASK_RUNS can be added into a function to avoid hardcoded values
//List task runs returns dbms_cloud_oci_di_data_integration_list_task_runs_response_t
getTasks := DBMS_CLOUD_OCI_DI_DATA_INTEGRATION.LIST_TASK_RUNS(workspace_id => '<your workspace ID>',
    application_key => '<Application key>', region => '<Region name Example: us-ashburn-1>', credential_name=>'<your credential ID>'); 
//Saving the response body with all list tasks
getBody := getTasks.response_body;
getListTaskSummary := getBody.items;

//Iterating over tasks (items)
FOR i IN 1..getListTaskSummary.COUNT LOOP
//we are only interested in update the manage_etl table with the task key from our pipeline
    IF getListTaskSummary(i).key = task_run_key AND getListTaskSummary(i).status = 'RUNNING' then
        EXECUTE IMMEDIATE 'UPDATE MANAGE_ETL SET STATUS = ' || '''' || STATUS || ''''  
        || ',ERROR_MESSAGE=' || '''' || ERROR_MESSAGE || ''''
        || ',NUM_ROWS=' || '''' || NO_OF_INSERTS || ''''
        || ',DURATION=' || '''' || DURATION || ''''
        || ',START_TIME=' || '''' || START_TIME || ''''
        || ',END_TIME=' || '''' || END_TIME || ''''
        || ' where task_key = ' || '''' || task_run_key || '''';
    end if;
  END LOOP;
end UPDATE_LOAD_STATUS;
