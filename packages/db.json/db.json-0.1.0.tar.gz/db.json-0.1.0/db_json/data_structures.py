from typing import Dict, List, Union

from pydantic import BaseModel


class RouteModel(BaseModel):
    path: str
    response: Union[List, Dict]


class RoutesMap(BaseModel):
    routes: List[RouteModel]
