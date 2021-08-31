from __future__ import print_function
import io
import os
import json
import sys
import oci
from oci.object_storage import UploadManager
from oci.object_storage.models import CreateBucketDetails
from oci.object_storage.transfer.constants import MEBIBYTE
import ftplib
from ftplib import FTP
from io import StringIO
from io import BytesIO
from fdk import response

filename = 'file name'
result =""
storetodir="/tmp"

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    try:
        
        body = json.loads(data.getvalue())
    except Exception:
        raise Exception('Error')

    workspace_id = "ocid1.disworkspace.oc1...."
    application_key="your application key...."
    # Get the task id from the event
    task_key = body.get("data").get("resourceId")
    dip = oci.data_integration.DataIntegrationClient(config={}, signer=signer)
    truns = dip.list_task_runs(workspace_id,application_key,aggregator_key=task_key, limit=1)
    for trun in truns.data.items:
      task_run_key = trun.key

      tr = dip.get_task_run(workspace_id,application_key, task_run_key=task_run_key)
      # If not SUCCESS - then this is a no-op
      if (tr.data.status != "SUCCESS"):
        resp_data = {"status":"200"}
        return response.Response(
            ctx, response_data=resp_data, headers={"Content-Type": "application/json"}
        )

    resp = manageFilesObjStorage()

    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

class SmartFTP(FTP):
    def makepasv(self):
        invalidhost, port = super(SmartFTP, self).makepasv()
        return self.host, port

def progress_callback(bytes_uploaded):
    print("{} additional bytes uploaded".format(bytes_uploaded))


def openConnectionFTP():
    ftp = SmartFTP('<ip or host>')
    ftp.login('<user>','<password>')
    r = BytesIO()
    os.chdir(storetodir)
    with open(filename, "wb") as file:
        ftp.retrbinary('RETR /<file name>', file.write)


def manageFilesObjStorage():
    openConnectionFTP()
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    bucket_name = "<bucket source>"
    bucket_name_target ="<bucket target>"
    object_name = "<file name>"
    result = "Uploading new object '" + object_name + "' in bucket '" + bucket_name_target + "'"
    part_size = 2 * MEBIBYTE  # part size (in bytes)
    upload_manager = UploadManager(client, allow_parallel_uploads=True, parallel_process_count=3)
    response = upload_manager.upload_file(
        namespace, bucket_name, object_name, filename, part_size=part_size, progress_callback=progress_callback)

    client.copy_object(namespace,bucket_name,
    oci.object_storage.models.CopyObjectDetails(
    source_object_name =        object_name,
    destination_bucket =        bucket_name_target,
    destination_region =        'eu-frankfurt-1',
    destination_namespace =     namespace,
    destination_object_name =   object_name     )
    )

    # remove file to clean up
    #os.remove(filename)

    print("Deleting object {}".format(object_name))
    #client.delete_object(namespace, bucket_name, object_name)
    return { "state": result }
