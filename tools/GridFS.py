from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from datetime import datetime
import base64

def base64_to_objectid(base64_string):
    """
    Converts a base64 encoded string back to a bson.ObjectId.

    Args:
        base64_string: The base64 encoded string representing the ObjectId.

    Returns:
        bson.ObjectId: The ObjectId object, or None if conversion fails.
    """
    try:
        decoded_bytes = base64.b64decode(base64_string)
        if len(decoded_bytes) != 12:
            raise ValueError("Decoded bytes are not 12 bytes long, not a valid ObjectId")
        object_id = ObjectId(decoded_bytes)
        return object_id
    except Exception as e:
        print(f"Error converting base64 to ObjectId: {e}")
        return None

class GridFSTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        client = MongoClient(self.runtime.credentials["uri"],
                    username=self.runtime.credentials["username"],
                    password=self.runtime.credentials["password"])
        db = client[tool_parameters["database_name"]]
        gridfs = GridFS(db, tool_parameters["collection_name"])
        out = gridfs.get(base64_to_objectid(tool_parameters["file_id"]))
        binary_data = out.read()
        output_format = tool_parameters.get("output_type", "text")
        client.close()
        if output_format == "files":
            yield self.create_blob_message(binary_data)
        else:
            base64_string = base64.b64encode(binary_data).decode('utf-8')
            yield self.create_text_message(base64_string)

