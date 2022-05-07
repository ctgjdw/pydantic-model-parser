from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydash import objects

from model_parser.custom_types import Mapping, MappingError


class BaseMapper(ABC):
    """
    An abstract base class that should be extended and implemented
    by an EntityMapper class. The class stores the mappings in the `get_mapping`
    function.

    The `get_mapping` function will store an array of tuples as defined here:
        - (`old_field_path`: str, `new_field_path`: str, `transform_func`: Optional[Callable])
    """

    @staticmethod
    @abstractmethod
    def get_mapping() -> List[Mapping]:
        """
        Abstract static function containing the list of mappings, to be defined by the
        implementing class and is used by the transform function to transform raw data.

        Returns:
            List[Mapping]: List of `(old_field_path, new_field_path, transform_func)` mappings
        """
        raise NotImplementedError()

    @classmethod
    def transform(cls, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Performs transformations on the input dictionary using the provided mappings in the `get_mapping` function.


        Args:
            data (Dict[Any, Any]): The original raw data object.

        Returns:
            Dict[Any, Any]: The transformed data object.

        Raise:
            MappingError: Raised if the an `old_field_path` in the mapping tuple is invalid
        """
        result = {}
        for old_field_path, new_field_path, transform_func in cls.get_mapping():
            if not objects.has(data, old_field_path):
                raise MappingError(
                    f"Invalid mapping, old_field_path does not exist for: {old_field_path}"
                )

            old_val = objects.get(data, old_field_path)
            objects.set_(
                result,
                new_field_path,
                transform_func(old_val) if transform_func else old_val,
            )
        return result
