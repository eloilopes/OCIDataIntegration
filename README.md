### OCI Data Integration - Handling parameters

1 - The first task (LOAD_ETL_PARAMETERS) is going to receive 2 parameters (TABLE_NAME and CODE). The source table name and country code. This procedure returns as output the target table name and country code.
It's very important to set the value of these parameters with pipeline parameters. You must add 2 new parameters and select the option "Assign a parameter"


2 - The second task (UPDATE_ETL_PARAMETERS), updates the control table with the table name, task run key, code and status for the data flow will be executed in next step. The table name and code coming from previous task. The task run key is using the system parameters and the status is hardcoded with "RUNNING".

3 - The Data Flow (integration task) will receive the 2 parameters from previous operator (target table name and code). Create a new parameter (PAR_SOURCE_PIPELINE) and assign it to SOURCE_PARAM.

4 - The last step (UPDATE_LOAD_STATUS), we update the control table. To do that we list all run tasks and search for the task run key and for the status of the pipeline and we update table with all details from previous data flow.

### How to start the pipeline?

```sql
declare
  workspace_ocid VARCHAR2(100) := '<Workspace ID>';
  application_key VARCHAR2(100) := '<Application key>';
  task_key VARCHAR2(100) := '<Task key>';
  region VARCHAR2(30) := '<Region>'; --eg. us-ashburn-1
  cred VARCHAR2(30) := '<Credential>';
  task_run_key VARCHAR2(65);
  parameterJsonString VARCHAR2(4000);
  cursor c_pending_tables is Select * from pending_load_tables;
  c_var c_pending_tables%rowtype;
begin

open c_pending_tables;

loop
    fetch c_pending_tables into c_var;
    exit when c_pending_tables%NOTFOUND;
    
    if c_var.status = 'PENDING' then
        parameterJsonString := '{"PAR_TABLE_NAME":{"simpleValue":"' || c_var.TABLE_NAME_TARGET || '"},
          "PAR_CODE":{"simpleValue":"' || c_var.CODE || '"},
          "PAR_SOURCE_PIPELINE":{"rootObjectValue":{"modelType":"ENRICHED_ENTITY",
        "entity":{"modelType":"TABLE_ENTITY","key":"dataref:<connction key>/<schema name>/TABLE_ENTITY:' || c_var.TABLE_NAME_SOURCE || '", "objectStatus" : 1}}}
          }';
          task_run_key := di_task_execute_params(workspace_ocid, application_key, task_key, region, cred, parameterJsonString);
          update pending_load_tables set status = 'EXECUTED' WHERE table_name_source=c_var.TABLE_NAME_SOURCE AND table_name_target=c_var.TABLE_NAME_TARGET
          AND CODE=c_var.CODE;
          COMMIT;
    end if;
end loop;
end;

```
