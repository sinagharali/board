from boto3 import client

from bucket.config import bucket_settings


class BucketClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            # Create the client
            cls._instance = client(
                "s3",
                endpoint_url=bucket_settings.endpoint,
                aws_access_key_id=bucket_settings.access_key,
                aws_secret_access_key=bucket_settings.secret_key,
            )

        return cls._instance
