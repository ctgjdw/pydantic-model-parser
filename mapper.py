from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydash import objects

from custom_types import Mapping

# class MappingError(Exception):
#     pass


class BaseMapper(ABC):
    @staticmethod
    @abstractmethod
    def get_mapping() -> List[Mapping]:
        """
        Abstract static property containing the list of mappings, implemented as a
        method as a workaround.

        Returns:
            List[Mapping]: List of `(new_field, old_field, transform_func)` mappings
        """        
        raise NotImplementedError()


    def transform(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Performs the JSON transformation from raw objects into our custom mappings.


        Args:
            data (Dict[Any, Any]): The original raw data object.

        Returns:
            Dict[Any, Any]: The transformed data object.
        """ 
        result = {}
        for new_key, old_key, transform in self.get_mapping():
            old_val = objects.get(data, old_key)
            
            # Uncommented this snippet, some values may be intentionally left as null
            # and we might want to capture that.

            # if not old_val:
            #     raise MappingError(f"Invalid mapping key: {old_key}")
            
            objects.set_(result, new_key, transform(
                old_key) if transform else old_val)
        return result
