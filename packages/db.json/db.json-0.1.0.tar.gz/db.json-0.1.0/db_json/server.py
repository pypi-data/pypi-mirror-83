import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from db_json.core import Core
from db_json.data_structures import RouteModel


def get_route(route: RouteModel) -> Route:
    async def view(request: Request) -> Response:
        return JSONResponse(route.response)

    return Route(f"/{route.path}", view)


async def index_view(request: Request) -> Response:
    routes = [route.path for route in request.app.routes]
    return JSONResponse(
        {
            "routes": routes,
        }
    )


class Server:
    def __init__(self, core: Core):
        routes = [Route("/", index_view)]
        for route in core.routes_map.routes:
            routes.append(get_route(route))
        self.app = Starlette(routes=routes)
        self.core = core

    def run(self, host: str, port: int) -> None:
        uvicorn.run(
            self.app,
            host=host,
            port=port,
        )
