from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

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
        df_list = []
        for item in items:
            df_dict = {}
            for key,value in item.items():
                if isinstance(value, ObjectId):
                    df_dict[key] = value.binary
                elif isinstance(value, datetime):
                    df_dict[key] = str(value)
                elif isinstance(value, (str,int,bool)):
                    df_dict[key] = value
                elif isinstance(value, list):
                    dl = []
                    for v in value:
                        if isinstance(v, ObjectId):
                            dl.append(v.binary)
                        else:
                            dl.append(v)
                    df_dict[key] = dl
            df_list.append(df_dict)
        mongo_json = {"mongodb": df_list}
        yield self.create_text_message(str(mongo_json))
