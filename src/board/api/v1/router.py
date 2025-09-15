from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi_utils.cbv import cbv

from auth.provider import get_current_user
from board.dependencies import get_board_service
from board.schemas import CreateBoardDto, UpdateBoardDto
from board.service import BoardService
from user.model import User

router = APIRouter(prefix="/boards", tags=["Board"])


@cbv(router)
class BoardCBV:
    def __init__(
        self,
        board_service: Annotated[BoardService, Depends(get_board_service)],
    ):
        self.board_service = board_service

    @router.post("/")
    async def create_board(
        self,
        user: Annotated[User, Depends(get_current_user)],
        dto: CreateBoardDto,
    ):
        return await self.board_service.create_board(user, dto)

    @router.patch("/{board_id}")
    async def update_board_info(
        self,
        board_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        dto: UpdateBoardDto,
    ):
        return await self.board_service.update_board(board_id, user, dto)

    @router.post("/{board_id}/avatar")
    async def set_avatar(
        self,
        board_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        avatar: UploadFile,
    ):
        return await self.board_service.set_avatar(board_id, user, avatar)

    @router.delete("/{board_id}/avatar")
    async def delete_avatar(
        self,
        board_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ):
        return await self.board_service.delete_avatar(board_id, user)

    @router.get("/{board_id}")
    async def get_board(
        self,
        board_id: UUID,
    ): ...

    @router.get("/")
    async def get_boards(
        self,
    ): ...

    @router.delete("/{board_id}")
    async def delete_board(
        self,
        board_id: UUID,
    ): ...
