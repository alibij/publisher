import re
from functools import lru_cache
from fastapi.openapi.utils import get_openapi
import abc


class Accessibility(metaclass=abc.ABCMeta):
    all = []

    @abc.abstractmethod
    def build(routes):
        Accessibility.all = routes


@lru_cache()
def get_routes(app):
    open_api = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )

    extra = []

    for path, methods in open_api['paths'].items():
        if not re.match(r'^/v[1-9]+/pa/', path):
            continue

        for _, val in methods.items():
            method_name = val['summary'].replace(' ', '_').lower()

            if method_name in [
                'panel_admins_auth_phone_number_post',
                'panel_admins_auth_login_post',
                'favicon', 'openapi',
                'root', 'ping'
            ]:
                continue

            extra.append(method_name)

    Accessibility.build(extra)
