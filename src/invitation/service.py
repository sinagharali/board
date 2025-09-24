from datetime import datetime, timezone
from uuid import UUID, uuid4

from acl.enums import ObjectType, Relation
from acl.errors import ACLError, ACLErrors
from acl.model import ACLTuple
from acl.openfga_authorization import AuthorizationService
from board.service import BoardService
from invitation.errors import InvitationError, InvitationErrors
from invitation.model import Invitation
from invitation.repository import InvitationRepository
from invitation.schemas import CreateInvitationDto
from membership.service import MembershipService
from user.model import User
from user.service import UserService


class InvitationService:
    def __init__(
        self,
        invitation_repo: InvitationRepository,
        authorization_service: AuthorizationService,
        user_service: UserService,
        membership_service: MembershipService,
        board_service: BoardService,
    ):
        self.invitation_repo = invitation_repo
        self.authorization_service = authorization_service
        self.user_service = user_service
        self.membership_service = membership_service
        self.board_service = board_service

    async def create_invitation(
        self,
        dto: CreateInvitationDto,
        user: User,
        board_id: UUID,
    ):
        # Check the board exist
        await self.board_service.ensure_board_exists(board_id)

        # Check if user can invite or not.
        can = await self.authorization_service.can(
            user.id_,
            board_id,
            ObjectType.BOARD,
            Relation.INVITE_USERS,
        )

        if not can:
            raise ACLError(ACLErrors.UNATHORIZED_ACTION)

        # Check the invitee exists.
        invitee_user = await self.user_service.ensure_user_exists_by_email(
            dto.invitee_email,
        )

        # Ensure user is not part the member of that board.
        await self.membership_service.ensure_user_is_not_member(
            invitee_user.id_,
            board_id,
        )

        # Ensure any active invite never send before.
        old_invitation = await self.invitation_repo.get_by_target_and_invited_by(
            board_id,
            user.id_,
        )

        if old_invitation:
            raise InvitationError(InvitationErrors.ALREADY_INVITED)

        # Create invitation
        invitation = await self.invitation_repo.create(
            Invitation(
                id_=uuid4(),
                invited_by=user.id_,
                invitee_email=dto.invitee_email,
                target_id=board_id,
                created_at=datetime.now(timezone.utc),
            ),
        )

        # Create the acl tuples
        await self.authorization_service.store_tuples(
            [
                # First Add Relation between board and the invitation
                ACLTuple(
                    user_type=ObjectType.BOARD,
                    user_id=board_id,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.BOARD,
                ),
                # Second, Add Relation between the user who invited to the board and the invitation
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=user.id_,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITED_BY,
                ),
                # Third, Add Relation between the invitee and the invitation
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=invitee_user.id_,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITEE,
                ),
            ],
        )

        return {"message": "invitation sent successfully"}

    async def delete_invitation(
        self,
        invitation_id: UUID,
        board_id,
        user: User,
    ):
        # Ensure we have a board with this id or not.
        await self.ensure_board_exists(board_id)

        # Check if user can delete invitation or not.
        can = await self.authorization_service.can(
            user.id_,
            invitation_id,
            ObjectType.INVITATION,
            Relation.CAN_DELETE,
        )

        if not can:
            raise ACLError(ACLErrors.UNATHORIZED_ACTION)

        # Check the invitation exist.
        invitation = await self.invitation_repo.get(
            model=Invitation,
            id_=invitation_id,
        )

        if not invitation:
            raise InvitationError(InvitationErrors.INVITATION_NOT_FOUND)

        # Get the invitee.
        invitee_user = await self.user_service.ensure_user_exists_by_email(
            invitation.invitee_email,
        )

        # Delete the acl tuples
        await self.authorization_service.delete_tuples(
            [
                ACLTuple(
                    user_type=ObjectType.BOARD,
                    user_id=board_id,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.BOARD,
                ),
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=user.id_,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITED_BY,
                ),
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=invitee_user.id_,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITEE,
                ),
            ],
        )
        await self.invitation_repo.delete(invitation)

        return {"message": "invitation deleted successfully"}

    async def accept_invitation(
        self,
        user: User,
        board_id: UUID,
        invitation_id: UUID,
    ):
        # Ensure we have a board with this id or not.
        await self.ensure_board_exists(board_id)

        # Check if user can accept the invitation or not.
        can = await self.authorization_service.can(
            user.id_,
            invitation_id,
            ObjectType.INVITATION,
            Relation.JOIN,
        )

        if not can:
            raise ACLError(ACLErrors.UNATHORIZED_ACTION)

        # Check the invitation exist.
        invitation = await self.invitation_repo.get(
            model=Invitation,
            id_=invitation_id,
        )

        if not invitation:
            raise InvitationError(InvitationErrors.INVITATION_NOT_FOUND)

        # Delete the acl tuples
        await self.authorization_service.delete_tuples(
            [
                ACLTuple(
                    user_type=ObjectType.BOARD,
                    user_id=board_id,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.BOARD,
                ),
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=invitation.invited_by,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITED_BY,
                ),
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=user.id_,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITEE,
                ),
            ],
        )
        # delete invitation
        await self.invitation_repo.delete(invitation)

        # Create membership for that board
        await self.membership_service.create_membership(board_id, user.id_)

        return {"message": "Invitation accepted!"}

    async def reject_invitation(
        self,
        user: User,
        board_id: UUID,
        invitation_id: UUID,
    ):
        # Ensure we have a board with this id or not.
        await self.ensure_board_exists(board_id)

        # Check if user can accept the invitation or not.
        can = await self.authorization_service.can(
            user.id_,
            invitation_id,
            ObjectType.INVITATION,
            Relation.JOIN,
        )

        if not can:
            raise ACLError(ACLErrors.UNATHORIZED_ACTION)

        # Check the invitation exist.
        invitation = await self.invitation_repo.get(
            model=Invitation,
            id_=invitation_id,
        )

        if not invitation:
            raise InvitationError(InvitationErrors.INVITATION_NOT_FOUND)

        # Delete the acl tuples
        await self.authorization_service.delete_tuples(
            [
                ACLTuple(
                    user_type=ObjectType.BOARD,
                    user_id=board_id,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.BOARD,
                ),
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=invitation.invited_by,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITED_BY,
                ),
                ACLTuple(
                    user_type=ObjectType.USER,
                    user_id=user.id_,
                    object_id=invitation.id_,
                    object_type=ObjectType.INVITATION,
                    relation=Relation.INVITEE,
                ),
            ],
        )
        # delete invitation
        await self.invitation_repo.delete(invitation)

        return {"message": "Invitation rejected!"}
