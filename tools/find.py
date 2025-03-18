from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import base64
import ast

def convert_bytes_to_str(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')  # 使用 base64 编码 bytes
    elif isinstance(obj, ObjectId):
        return base64.b64encode(obj.binary).decode('utf-8')
    elif isinstance(obj, datetime):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convert_bytes_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_bytes_to_str(item) for item in obj]
    else:
        return obj

class FindTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        client = MongoClient(self.runtime.credentials["uri"],
                    username=self.runtime.credentials["username"],
                    password=self.runtime.credentials["password"])
        db = client[tool_parameters["database_name"]]
        collection = db[tool_parameters["collection_name"]]
        print((tool_parameters["query"]))
        items = collection.find(eval(tool_parameters["query"]))
        items = list(items)
        json_mongodb_list = convert_bytes_to_str(items)
        client.close()
        output_format = tool_parameters.get("output_type", "text")
        if output_format == "text":
            yield self.create_text_message(str(json_mongodb_list))
        else:
            yield self.create_json_message({
                "result": json_mongodb_list
            })
