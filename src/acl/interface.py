from abc import ABC, abstractmethod
from uuid import UUID

from acl.enums import ObjectType, Relation


class IAuthorizationService(ABC):
    @abstractmethod
    async def can(self, user_id: UUID, object_type: ObjectType, relation: Relation):
        pass

    @abstractmethod
    async def store_tuple(
        self,
        user_id: UUID,
        object_id: UUID,
        object_type: ObjectType,
        relation: Relation,
    ):
        pass
