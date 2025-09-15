from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from auth.config import auth_settings as settings
from auth.dependencies import get_auth_service
from auth.schemas import SigninDto, SignupDto
from auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@cbv(router)
class AuthCBV:
    def __init__(self, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
        self.auth_service = auth_service

    @router.post("/signup")
    async def signup(self, req: Request, dto: SignupDto):
        result = await self.auth_service.signup(req, dto)

        resp = JSONResponse(
            content={
                "accessToken": result["access"],
                "user": result["user"],
            },
        )

        resp.set_cookie(
            key="refresh_token",
            value=result["refresh"],
            max_age=timedelta(
                days=settings.refresh_token_expire_days,
            ).total_seconds(),
            expires=datetime.now(timezone.utc) + timedelta(days=7),
            httponly=True,
            secure=req.url.scheme == "https",
            samesite="Strict",
        )

        return resp

    @router.post("/signin")
    async def signin(self, req: Request, dto: SigninDto):
        result = await self.auth_service.signin(req, dto)

        resp = JSONResponse(
            content={
                "accessToken": result["access"],
                "user": result["user"],
            },
        )

        resp.set_cookie(
            key="refresh_token",
            value=result["refresh"],
            max_age=timedelta(
                days=settings.refresh_token_expire_days,
            ).total_seconds(),
            expires=datetime.now(timezone.utc) + timedelta(days=7),
            httponly=True,
            secure=req.url.scheme == "https",
            samesite="Strict",
        )

        return resp

    @router.post("/refresh")
    async def refresh(self, req: Request):
        refresh_token = req.cookies.get("refresh_token")

        result = await self.auth_service.refresh(refresh_token)

        resp = JSONResponse(
            content={
                "accessToken": result["access"],
                "user": result["user"],
            },
        )

        resp.set_cookie(
            key="refresh_token",
            value=result["refresh"],
            max_age=timedelta(
                days=settings.refresh_token_expire_days,
            ).total_seconds(),
            expires=datetime.now(timezone.utc) + timedelta(days=7),
            httponly=True,
            secure=req.url.scheme == "https",
            samesite="Strict",
        )

        return resp

    @router.post("/signout")
    async def signout(self, req: Request, response: Response):
        refresh_token = req.cookies.get("refresh_token")

        await self.auth_service.signout(refresh_token)

        # Clear the cookie
        response.delete_cookie("refresh_token")
        return {"message": "signed out successfully"}
