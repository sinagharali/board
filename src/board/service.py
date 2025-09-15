from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import UploadFile

from acl.enums import ObjectType, Relation
from acl.errors import ACLError, ACLErrors
from acl.openfga_authorization import AuthorizationService
from board.errors import BoardError, BoardErrors
from board.model import Board
from board.schemas import CreateBoardDto, UpdateBoardDto
from bucket.aws_service import BucketService
from common.validators.file import validate_image
from database.base_repo import BaseRepository
from user.model import User


class BoardService:
    def __init__(
        self,
        board_repo: BaseRepository,
        authorization_service: AuthorizationService,
        bucket_service: BucketService,
    ):
        self.board_repo = board_repo
        self.authorization_service = authorization_service
        self.bucket_service = bucket_service

    def _utc_now(self):
        return datetime.now(timezone.utc)

    async def create_board(
        self,
        user: User,
        dto: CreateBoardDto,
    ):
        # Each Authenticate User can create board for own self.

        # Create and store Board Model.
        now = self._utc_now()
        new_board = await self.board_repo.create(
            Board(
                id_=uuid4(),
                name=dto.name,
                caption=dto.caption,
                avatar=None,
                created_by=user.id_,
                created_at=now,
                updated_at=now,
            ),
        )
        # Store the tuple in openfga.
        await self.authorization_service.store_tuple(
            user.id_,
            new_board.id_,
            ObjectType.BOARD,
            Relation.OWNER,
        )

        # Return the created board.
        return {"board": new_board}

    async def update_board(
        self,
        board_id: UUID,
        user: User,
        dto: UpdateBoardDto,
    ):
        # Check if we have a board with this id or not.
        board = await self.board_repo.get(Board, board_id)

        if not board:
            raise BoardError(BoardErrors.BOARD_NOT_FOUND)

        # Check the ability that user can edit board or not.
        can = await self.authorization_service.can(
            user.id_,
            board_id,
            ObjectType.BOARD,
            Relation.CHANGE_INFO,
        )

        if not can:
            raise ACLError(ACLErrors.UNATHORIZED_ACTION)

        # Edit and update note
        update_data = dto.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )  # only fields sent by client that are not null too

        for field, value in update_data.items():
            setattr(board, field, value)

        await self.board_repo.update(board)

        # return the new board.
        return {"board": board}

    async def set_avatar(
        self,
        board_id: UUID,
        user: User,
        avatar: UploadFile,
    ):
        # Check is avatar valid or not.
        await validate_image(avatar)
        # Check if we have a board with this id or not.
        board = await self.board_repo.get(Board, board_id)

        if not board:
            raise BoardError(BoardErrors.BOARD_NOT_FOUND)

        # Check the ability that user can edit board or not.
        can = await self.authorization_service.can(
            user.id_,
            board_id,
            ObjectType.BOARD,
            Relation.CHANGE_INFO,
        )
        if not can:
            raise ACLError(ACLErrors.UNATHORIZED_ACTION)

        if board.avatar:
            # First delete the avatar
            await self.bucket_service.delete_file(board.avatar)

        # upload the new avatar
        file_name = f"Board-{uuid4()}"

        await self.bucket_service.upload_file(avatar, file_name)

        # update the board
        board.avatar = file_name
        await self.board_repo.update(board)

    async def delete_avatar(
        self,
        board_id: UUID,
        user: User,
    ):
        # Check if we have a board with this id or not.
        board = await self.board_repo.get(Board, board_id)

        if not board:
            raise BoardError(BoardErrors.BOARD_NOT_FOUND)

        # Check the ability that user can edit board or not.
        can = await self.authorization_service.can(
            user.id_,
            board_id,
            ObjectType.BOARD,
            Relation.CHANGE_INFO,
        )
        if not can:
            raise ACLError(ACLErrors.UNATHORIZED_ACTION)

        if not board.avatar:
            return {"message": "avatar is already empty"}

        # Delete the avatar
        await self.bucket_service.delete_file(board.avatar)
        return None
