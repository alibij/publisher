from fastapi import APIRouter, Depends
from common.jwt_bearer import JWTBearer, check_user_pass

# Import routers

from .Panel.file_handler import PA_FileHandler_router
from .Panel.publish import PA_Publish_router


public_routers = []

panel_routers = [
    (PA_FileHandler_router, "FileHandler"),
    (PA_Publish_router, "Publish")
]


oauth2_scheme = JWTBearer()
# depend_list = [Depends(oauth2_scheme)]
depend_list = [Depends(check_user_pass)]

version_routers = APIRouter(prefix="/v1")


def include_routers(router_list, prefix="", dependencies=None):
    for router, tag in router_list:
        version_routers.include_router(
            router, prefix=prefix, dependencies=dependencies, tags=[tag]
        )


include_routers(public_routers)

include_routers(panel_routers, prefix="", dependencies=depend_list)
