from fastapi import APIRouter, Depends
from common.jwt_bearer import JWTBearer

# Import routers

from .Panel.access_maneger import PA_AdminUser_router
from .Panel.homePage import PA_HomePageSlider_router
from .Panel.about import PA_About_router
from .Panel.file_handler import PA_FileHandler_router
from .Panel.product import PA_Product_router
from .Panel.blog import PA_Blog_router
from .Panel.roadMap import PA_RoadMap_router
from .Panel.service import PA_Service_router

from .Public.access_maneger import Login_router
from .Public.homePage import HomePageSlider_router
from .Public.about import About_router
from .Public.product import Product_router
from .Public.blog import Blog_router
from .Public.roadMap import RoadMap_router
from .Public.service import Service_router


public_routers = [
    (Login_router, "Login"),
    (HomePageSlider_router, "HomePage"),
    (About_router, "About"),
    (Product_router, "Products"),
    (Blog_router, "Blogs"),
    (RoadMap_router, "RoadMap"),
    (Service_router, "Service"),
]

panel_routers = [
    (PA_AdminUser_router, "Admin"),
    (PA_HomePageSlider_router, "HomePage"),
    (PA_About_router, "About"),
    (PA_Product_router, "Products"),
    (PA_Blog_router, "Blogs"),
    (PA_RoadMap_router, "RoadMap"),
    (PA_Service_router, "Service"),
    (PA_FileHandler_router, "FileHandler"),
]


oauth2_scheme = JWTBearer()
depend_list = [Depends(oauth2_scheme)]

version_routers = APIRouter(prefix="/v1")


def include_routers(router_list, prefix="", dependencies=None):
    for router, tag in router_list:
        version_routers.include_router(
            router, prefix=prefix, dependencies=dependencies, tags=[tag]
        )


include_routers(public_routers)

include_routers(panel_routers, prefix="/pa", dependencies=depend_list)
