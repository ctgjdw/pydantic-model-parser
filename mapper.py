from typing import List
from pydash import objects

from custom_types import Mapping

class MappingError(Exception):
    pass


class EntityMapper:
    def __init__(self, mappings: List[Mapping]):
        self.mappings = mappings

    def transform(self, data: dict) -> dict:
        result = {}
        for new_key, old_key, mapping_func in self.mappings:
            old_val = objects.get(data, old_key)
            if not old_val:
                raise MappingError(f"Invalid mapping key: {old_key}")
            objects.set_(result, new_key, mapping_func(
                old_key) if mapping_func else old_val)
        return result
