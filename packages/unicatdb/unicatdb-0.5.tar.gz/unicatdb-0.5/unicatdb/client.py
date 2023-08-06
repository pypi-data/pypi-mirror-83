from .openapi_client import FindingsApi, ApiClient, ChartsApi, AttachmentsApi, SchemasApi, SecurityApi, ExportApi
from . import Configuration


class Client():

    def __init__(self, configuration: Configuration) -> None:
        super().__init__()

        self.__configured_api_client = ApiClient(configuration)

    # support for with() statement
    def __enter__(self):
        self.__configured_api_client.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__configured_api_client.__exit__(exc_type, exc_value, traceback)

    def close(self):
        self.__configured_api_client.close()

    # individual APIs as configured properties:

    @property
    def attachments(self):
        return AttachmentsApi(self.__configured_api_client)

    @property
    def charts(self):
        return ChartsApi(self.__configured_api_client)

    @property
    def export(self):
        return ExportApi(self.__configured_api_client)

    @property
    def findings(self):
        return FindingsApi(self.__configured_api_client)

    @property
    def schemas(self):
        return SchemasApi(self.__configured_api_client)

    @property
    def security(self):
        return SecurityApi(self.__configured_api_client)
