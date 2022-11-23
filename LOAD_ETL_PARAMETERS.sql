CREATE OR REPLACE PROCEDURE "ADMIN"."LOAD_ETL_PARAMETERS" 
(SOURCE IN VARCHAR2, TABLE_NAME IN VARCHAR2, MAX_LOAD_DATE OUT DATE, START_TIME OUT TIMESTAMP, 
END_TIME OUT TIMESTAMP, DURATION OUT INTEGER, NO_OF_INSERTS OUT INTEGER, 
STATUS OUT VARCHAR2, ERROR_MESSAGE OUT VARCHAR2 ) IS v_MAX_LOAD_DATE date; 

BEGIN EXECUTE IMMEDIATE 'SELECT MAX(trunc(LAST_LOAD_DATE)) from MANAGE_ETL where SOURCE = ' || '''' || 
SOURCE || '''' || ' AND TABLE_NAME = ' || '''' || TABLE_NAME || '''' 
into MAX_LOAD_DATE; 

END LOAD_ETL_PARAMETERS;	
