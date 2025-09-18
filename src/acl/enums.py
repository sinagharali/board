from enum import Enum


class ObjectType(str, Enum):
    BOARD = "board"
    USER = "user"
    NOTE = "note"


class Relation(str, Enum):
    # Board Relations
    ADD_ADMINS = "add_admins"
    ADMIN = "admin"
    CAN_CREATE_NOTE = "can_create_note"
    CHANGE_INFO = "change_info"
    CHANGE_OWNERSHIP = "change_ownership"
    INVITE_USERS = "invite_users"
    MANAGE_NOTES = "manage_notes"
    MEMBER = "member"
    OWNER = "owner"
    REMOVE_ADMIN = "remove_admin"
    REMOVE_MEMBER = "remove_member"
    VIEW = "view"

    # Note Relations
    BOARD = "board"
    CREATOR = "creator"
    CAN_DELETE = "can_delete"
    CAN_EDIT = "can_edit"
    CAN_VIEW = "can_view"

    # Invitation Relations
    # BOARD = "board"  --I put it there just for consistancy--
    INVITEE = "invitee"
    INVITED_BY = "invited_by"
    JOIN = "join"
    REJECT = "reject"
    # CAN_DELETE = "can_delete"
    # VIEW = "view"


OBJECT_RELATION_MAP = {
    ObjectType.BOARD: [
        Relation.ADD_ADMINS,
        Relation.ADMIN,
        Relation.CAN_CREATE_NOTE,
        Relation.CHANGE_INFO,
        Relation.CHANGE_OWNERSHIP,
        Relation.INVITE_USERS,
        Relation.INVITED,
        Relation.JOIN,
        Relation.MANAGE_NOTES,
        Relation.MEMBER,
        Relation.OWNER,
        Relation.REMOVE_ADMIN,
        Relation.REMOVE_MEMBER,
        Relation.VIEW,
    ],
    ObjectType.NOTE: [
        Relation.BOARD,
        Relation.CREATOR,
        Relation.CAN_DELETE,
        Relation.CAN_EDIT,
        Relation.CAN_VIEW,
    ],
    ObjectType.USER: [],
    ObjectType.INVITATION: [
        Relation.BOARD,
        Relation.INVITEE,
        Relation.INVITED_BY,
        Relation.JOIN,
        Relation.REJECT,
        Relation.CAN_DELETE,
        Relation.VIEW,
    ],
}
