from bucket.aws_service import BucketService
from bucket.client import BucketClientSingleton
from bucket.config import bucket_settings
from bucket.interface import IBucketService


def get_bucket_service() -> IBucketService:
    client = BucketClientSingleton.get_instance()
    bucket_service = BucketService(client, bucket_settings.name)
    return bucket_service
