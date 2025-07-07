from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from typing import Optional
import os
import datetime

class _S3Client:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def get_objects(self) -> list:
        response = self.s3_client.list_objects(Bucket=self.bucket_name)['Contents']
        files = []
        for file in response:
            files.append({"name": file['Key'].replace("/tmp/", ''), "size": file['Size'], "last_modified": file["LastModified"].strftime('%Y-%m-%d %H:%M')})

        return files

    def save(self, data: bytes, object_name: str | None) -> bool:
        """Save a bytes object to the S3 bucket."""
        if object_name is None:
            raise ValueError("Object name must be provided")
        try:
            self.s3_client.upload_fileobj(BytesIO(data), self.bucket_name, f'/tmp/{object_name}')
            return True
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Error uploading file: {e}")
            return False

    def download(self, object_name: str) -> dict:
        """Download a single file from the S3 bucket and return it as a FileResponse for FastAPI."""
        file_path = f"/tmp/{object_name}"
        file = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_path)
        return {
                "file_name": object_name,
                "path": file_path,
                "content": file, 
            }
        

    def download_multiple(self, object_names: list[str]) -> list[dict]:
        """Download multiple files from the S3 bucket"""
        responses = []
        for object_name in object_names:
            file_path = f"/tmp/{object_name}"
            file = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_path)
            file_dict = {
                "file_name": object_name,
                "path": file_path,
                "content": file, 
            }
            responses.append(file_dict)
        return responses
    
    def delete(self, object_names: list[str]):
        """Delete multiple files from the S3 bucket"""
        files = []
        for object_name in object_names:
            files.append({"Key": f'/tmp/{object_name}'})
        return self.s3_client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': files})


S3Client = _S3Client(
    endpoint=os.environ["S3_ENDPOINT"],
    access_key=os.environ["S3_ACCESS_KEY"],
    secret_key=os.environ["S3_SECRET_KEY"],
    bucket_name=os.environ["S3_BUCKET_NAME"],
)
