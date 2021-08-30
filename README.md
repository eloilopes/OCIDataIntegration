### OCI Data Integration

OCI Data Integration is a serverless ETL tool fully managed by Oracle. Right now, doesn't have a FTP connector out of box.

With this script you can connect to an FTP server, pick a file and Upload to OCI Object Storage Bucket, copy the same file to other bucket and delete the file in the end.

Policies that I used to be able to run this script on OCI Data Integration. **Before use these policies, check oracle documentation. I'm not responsible for the misuse of these policies in customer environments.**

**Policies for OCI Data Integration**
https://docs.oracle.com/en-us/iaas/data-integration/using/policies.htm

allow service dataintegration to use virtual-network-family in compartment <compartment>

allow group <group> to use object-family in compartment <compartment>

allow any-user to use buckets in compartment <compartment> where ALL {request.principal.type = 'disworkspace', request.principal.id = 'ocid1.disworkspace.oc1....'}

allow any-user to manage objects in compartment <compartment> where ALL {request.principal.type = 'disworkspace', request.principal.id = 'ocid1.disworkspace.oc1...'}

allow any-user {PAR_MANAGE} in compartment <compartment> where ALL {request.principal.type = 'disworkspace', request.principal.id = 'ocid1.disworkspace.oc1....'}


allow any-user to use fn-invocation in compartment <compartment> where ALL {request.principal.type='disworkspace', request.principal.id='ocid1.disworkspace.oc1.eu-frankfurt-1…..'}

allow any-user to read fn-function in compartment <compartment>where ALL {request.principal.type='disworkspace', request.principal.id='ocid1.disworkspace.oc1.eu-frankfurt-1….'}


**Policies OCI Functions**
https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartcloudshell.htm#functionsquickstart_cloudshell


Allow group <group-name> to use cloud-shell in tenancy

Allow group <group-name> to manage repos in tenancy

Allow group <group-name> to read objectstorage-namespaces in tenancy

Allow group <group-name> to manage logging-family in tenancy

Allow group <group-name> to read metrics in tenancy

Allow group <group-name> to manage functions-family in tenancy

Allow group <group-name> to use virtual-network-family in tenancy

Allow group <group-name> to use apm-domains in tenancy

Allow service faas to use apm-domains in tenancy

