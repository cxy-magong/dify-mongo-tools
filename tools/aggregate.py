from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import base64
import json

def convert_bytes_to_str(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
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

class AggregateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        client = MongoClient(
            self.runtime.credentials["uri"],
            username=self.runtime.credentials["username"],
            password=self.runtime.credentials["password"]
        )
        
        # 获取数据库和集合
        db = client[tool_parameters["database_name"]]
        collection = db[tool_parameters["collection_name"]]
        print(tool_parameters["pipeline"])
        # 解析聚合管道
        pipeline = json.loads(tool_parameters["pipeline"])
        
        # 执行聚合操作
        cursor = collection.aggregate(pipeline)
        results = list(cursor)
        
        # 转换数据类型
        converted_results = convert_bytes_to_str(results)
        
        # 根据输出格式返回结果
        output_format = tool_parameters.get("output_type", "text")
        if output_format == "text":
            yield self.create_text_message(str(converted_results))
        else:
            yield self.create_json_message({
                "result": converted_results
            })