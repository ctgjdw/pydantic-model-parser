from typing import List, Dict, Any, Union, overload
from custom_types import JsonObject
from mapper import BaseMapper
from pydantic import BaseModel

class Parser:
    def __init__(self, entity:BaseModel, mapper: BaseMapper) -> None:
        self._entity = entity
        self._mapper = mapper

    @overload
    def parse(self, raw: JsonObject) -> BaseModel:
        ...

    @overload
    def parse(self, raw: List[JsonObject]) -> List[BaseModel]:
        ...

    def parse(self, raw:Union[JsonObject, List[JsonObject]]) -> Union[BaseModel, List[BaseModel]]:
        if isinstance(raw, dict):
            parsed = self._mapper.transform(raw)
            return self._entity.parse_obj(parsed)

        parsed = [self._mapper.transform(item) for item in raw]
        return [self._entity.parse_obj(item) for item in parsed]

