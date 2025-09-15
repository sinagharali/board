from acl.client import OpenFgaClientSingleton
from acl.interface import IAuthorizationService
from acl.openfga_authorization import AuthorizationService


async def get_authorization_service() -> IAuthorizationService:
    client = await OpenFgaClientSingleton.get_instance()
    return AuthorizationService(client)
