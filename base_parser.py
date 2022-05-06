from mapper import BaseMapper
from pydantic import BaseModel

class BaseParser:
    def __init__(self, entity:BaseModel, mapper: BaseMapper) -> None:
        self._entity = entity
        self._mapper = mapper

    def apply_mapping(self, data: dict) -> dict:
        return self.entity_mapper.transform(data)

    def parse(self, data: dict) -> dict:
        parsed = self.apply_mapping(data)
        return self.entity_class.parse_obj(parsed)

    def parse_many(self, data_list: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
        return list(map(self.parse, data_list))
