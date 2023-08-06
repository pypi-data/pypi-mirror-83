import os
import socket
from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class NodeInfo(BaseModel):
    pid: str
    hostname: str


current_node = NodeInfo(pid=str(os.getpid()), hostname=socket.gethostname())


class Event(BaseModel):
    node_info: NodeInfo = Field(current_node)


class SQLQuery(Event):
    type: Literal["SQLQuery"] = Field("SQLQuery", const=True)
    sql: str
    duration: float
    db: str


class Request(Event):
    type: Literal["Request"] = Field("Request", const=True)
    path: str
    status_code: int
    time: float
    duration: float
    queries: List[SQLQuery] = []
    request_headers: Dict[str, str]
    response_headers: Dict[str, str]
