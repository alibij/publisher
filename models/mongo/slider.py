from pydantic import BaseModel
from typing import List


from db.mongo import SetEnum, Migration
from models.mongo import Collections


class SliderModel(BaseModel, metaclass=SetEnum):
    code: str = None
    seo_text: str = None
    seo_titel: str = None
    image_desktop: str = None
    image_mobile: str = None

    created_at: int = None
    updated_at: int = None

    class Config:
        collection = Collections.slider
        migrate = Migration(
            normal_index=[]
        )


migrate = [SliderModel]
