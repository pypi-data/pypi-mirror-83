import cv2 
import base64
import datetime
import numpy as np
from google.cloud import storage


def download_from_storage(bucket_name, source_blob_name, destination_file_name):
    """[Function to download object from google cloud storage to local]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        source_blob_name {[string]} -- [Path to object in google cloud storage]
        destination_file_name {[string]} -- [Name and Path object in local]
    
    Returns:
        object  -- [Downloaded object from storage]
    """    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def generate_upload_signed_url(bucket_name, blob_name):
    
    """Generates a v4 signed URL for uploading a blob using HTTP PUT.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",   
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow PUT requests using this URL.
        method="PUT",
        content_type="application/octet-stream",
    )

    return url


def generate_download_signed_url(bucket_name, blob_name):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )

    return url


def upload_to_storage(bucket_name, file_bytes, destination_blob_name, content_type):
    """[Function to upload object from local to google cloud storage]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        file_bytes {[bytes]} -- [Bytes of object that want to upload to google cloud storage]
        destination_blob_name {[string]} -- [Name and Path object in google cloud storage]
        content_type {[string]} -- [Type of data to save object in google cloud storage]
    """    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_bytes, content_type=content_type)


def read_image_gcs_b64(bucket, image_file): 
    """[summary]

    Args:
        bucket ([type]): [description]
        image_file ([type]): [description]

    Returns:
        [type]: [description]
    """    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(image_file)

    blob_array = np.asarray(bytearray(blob.download_as_string()), 
                                dtype=np.uint8)
    img_np = cv2.imdecode(blob_array, cv2.IMREAD_COLOR)
    if img_np is None: 
        img_np = cv2.imdecode(blob_array, cv2.IMREAD_UNCHANGED)
    img_jpg = cv2.imencode('.jpeg', img_np)[1]
    image_b64 = base64.b64encode(img_jpg).decode('utf-8')
    return image_b64
