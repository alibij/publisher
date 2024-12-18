
from pydantic import BaseModel


class PublishPostIn (BaseModel):
    project_name: str
    backup: bool = True
    args: list[str] = None
