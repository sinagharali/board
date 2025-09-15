from openfga_sdk import ClientConfiguration, OpenFgaClient

from acl.config import acl_settings


class OpenFgaClientSingleton:
    _instance: OpenFgaClient = None

    @classmethod
    async def get_instance(cls) -> OpenFgaClient:
        if cls._instance is None:
            config = ClientConfiguration(
                api_url=acl_settings.api_url,
                store_id=acl_settings.store_id,
                authorization_model_id=acl_settings.model_id,
            )

            cls._instance = await OpenFgaClient(config).__aenter__()
        return cls._instance

    @classmethod
    async def close(cls):  # Close when the app lifetime end.
        if cls._instance:
            await cls._instance.__aexit__(None, None, None)
            cls._instance = None
