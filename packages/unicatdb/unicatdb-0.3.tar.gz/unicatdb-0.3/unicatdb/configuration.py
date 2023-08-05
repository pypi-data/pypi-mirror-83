from .openapi_client import Configuration as OpenapiConfiguration
from .servers import Servers

class Configuration(OpenapiConfiguration):

    def __init__(self, api_key, access_token=None, server: Servers = Servers.UNICATDB_ORG):
        self.access_token = access_token
        super().__init__(
            host=server.value,
            api_key={
                'ApiKeyAuth': api_key
            })

    def auth_settings(self):
        auth = super().auth_settings()

        auth['JwtAuth'] = {
            'type': 'bearer',
            'in': 'header',
            'format': 'JWT',
            'key': 'Authorization',
            'value': 'Bearer ' + self.access_token
        }

        return auth


