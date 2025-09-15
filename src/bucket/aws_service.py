from boto3 import client
from fastapi.concurrency import run_in_threadpool

from bucket.errors import BucketError, BucketErrors
from bucket.interface import IBucketService
from logger import logger

URL_EXPIRATION_TIME = 3600


class BucketService(IBucketService):
    def __init__(self, client: client, bucket: str):
        self.client = client
        self.bucket = bucket

    async def upload_file(self, file_, file_name):
        try:
            await run_in_threadpool(
                lambda: self.client.upload_fileobj(file_, self.bucket, file_name),
            )
        except Exception as e:
            logger.error(f"exception: {e}")
            raise BucketError(BucketErrors.UPLOAD_FAILED) from e

    async def generate_presigned_url(
        self,
        file_name,
        expiration=URL_EXPIRATION_TIME,
    ):
        try:
            return await run_in_threadpool(
                self.client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket, "Key": file_name},
                    ExpiresIn=expiration,
                ),
            )
        except Exception as e:
            raise BucketError(BucketErrors.PRESIGNED_URL_FAILED) from e

    async def delete_file(self, file_name):
        try:
            await run_in_threadpool(
                self.client.delete_object(Bucket=self.bucket, Key=file_name),
            )
        except Exception as e:
            raise BucketError(BucketErrors.DELETE_FAILED) from e
