from enum import Enum
from pydantic import BaseModel
from db.mongo import SetEnum


class Collections(str, Enum):
    admin = 'admin'
    slider = 'slider'
    about = 'about'
    product = 'product'
    blog = 'blog'
    road_map = 'road_map'
    service = 'service'
