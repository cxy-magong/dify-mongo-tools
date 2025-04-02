from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from pymongo import MongoClient

class MongoProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            client = MongoClient(credentials["uri"],
                        username=credentials["username"],
                        password=credentials["password"])
            server_info = client.server_info()
            print("connect mongo_db Success:", server_info)
            client.close()
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
        finally:
            if "client" in locals():
                client.close()
