from uuid import UUID

from pydantic import BaseModel

from acl.enums import ObjectType, Relation


class ACLTuple(BaseModel):
    user_type: ObjectType
    user_id: UUID
    object_id: UUID
    object_type: ObjectType
    relation: Relation
