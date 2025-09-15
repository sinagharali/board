from abc import ABC, abstractmethod
from typing import BinaryIO


class IBucketService(ABC):
    @abstractmethod
    def upload_file(self, file: BinaryIO, file_name: str) -> None:
        pass

    @abstractmethod
    def generate_presigned_url(self, file_name: str, expiration: int = 3600) -> str:
        pass

    @abstractmethod
    def delete_file(self, file_name: str) -> None:
        pass
