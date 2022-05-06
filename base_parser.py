from typing import Tuple, Optional, Callable, List, Dict, Any
from mapper import EntityMapper
from pydantic import BaseModel


class BaseParser:
    def __init__(self, entity_class: BaseModel, mappings: Tuple[str, str, Optional[Callable]]):
        self.entity_mapper = EntityMapper(mappings)
        self.entity_class = entity_class

    def apply_mapping(self, data: dict) -> dict:
        return self.entity_mapper.transform(data)

    def parse(self, data: dict) -> dict:
        parsed = self.apply_mapping(data)
        return self.entity_class.parse_obj(parsed)

    def parse_many(self, data_list: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
        return list(map(self.parse, data_list))
