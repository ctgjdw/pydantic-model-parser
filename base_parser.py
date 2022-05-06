from typing import List, Dict, Any
from mapper import BaseMapper
from pydantic import BaseModel

class Parser:
    def __init__(self, entity:BaseModel, mapper: BaseMapper) -> None:
        self._entity = entity
        self._mapper = mapper

    def parse(self, raw:Dict[Any, Any]) -> BaseModel:
        parsed = self._mapper.transform(raw)
        return self._entity.parse_obj(parsed)

    def parse_many(self, data_list: List[Dict[Any, Any]]) -> List[BaseModel]:
        return list(map(self.parse, data_list))    

