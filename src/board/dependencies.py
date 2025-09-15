from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from acl.dependencies import get_authorization_service
from acl.openfga_authorization import AuthorizationService
from board.repository import BoardRepository
from board.service import BoardService
from bucket.aws_service import BucketService
from bucket.dependencies import get_bucket_service
from database.engine import get_session


async def get_board_service(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    authorization_service: Annotated[
        AuthorizationService,
        Depends(get_authorization_service),
    ],
    bucket_service: Annotated[BucketService, Depends(get_bucket_service)],
):
    board_repo = BoardRepository(db_session)
    return BoardService(
        board_repo=board_repo,
        authorization_service=authorization_service,
        bucket_service=bucket_service,
    )
