from uuid import UUID

from openfga_sdk import OpenFgaClient
from openfga_sdk.client import ClientCheckRequest
from openfga_sdk.client.models import ClientTuple, ClientWriteRequest

from acl.enums import OBJECT_RELATION_MAP, ObjectType, Relation
from acl.errors import ACLError, ACLErrors
from acl.interface import IAuthorizationService


class AuthorizationService(IAuthorizationService):
    def __init__(self, fga_client: OpenFgaClient):
        self.fga_client = fga_client

    def _validate_action(self, relation, object_type):
        if relation not in OBJECT_RELATION_MAP.get(object_type, []):
            raise ACLError(ACLErrors.ACTION_NOT_VALID)

    async def can(
        self,
        user_id: UUID,
        object_id: UUID,
        object_type: ObjectType,
        relation: Relation,
    ) -> bool:
        self._validate_action(relation, object_type)

        body = ClientCheckRequest(
            user=f"user:{user_id}",
            relation=f"{relation.value}",
            object=f"{object_type.value}:{object_id}",
        )

        response = await self.fga_client.check(body)
        return response.allowed

    async def store_tuple(
        self,
        user_id: UUID,
        object_id: UUID,
        object_type: ObjectType,
        relation: Relation,
    ):
        self._validate_action(relation, object_type)

        body = ClientWriteRequest(
            writes=[
                ClientTuple(
                    user=f"user:{user_id}",
                    relation=f"{relation.value}",
                    object=f"{object_type.value}:{object_id}",
                ),
            ],
        )

        await self.fga_client.write(body)  # this might throw, I should handle later.
