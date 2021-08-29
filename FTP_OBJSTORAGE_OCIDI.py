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

filename = '<your file>'
result =""
storetodir="/tmp"

def handler(ctx, data: io.BytesIO=None):

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
    ftp = SmartFTP('<FTP Host or IP>')
    ftp.login('<user>','<password>')
    r = BytesIO()
    os.chdir(storetodir)
    with open(filename, "wb") as file:
        ftp.retrbinary('RETR /<file>', file.write)


def manageFilesObjStorage():
    openConnectionFTP()
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    bucket_name = "<Source Bucket>"
    bucket_name_target ="<Target Bucket>"
    object_name = "<file>"
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
