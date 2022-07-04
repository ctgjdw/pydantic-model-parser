from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydash import objects

from model_parser.custom_types import Mapping, TransformFuncError


class BaseMapper(ABC):
    """
    An abstract base class that should be extended and implemented
    by an EntityMapper class. The class stores the mappings in the `get_mapping`
    function.

    The `get_mapping` function will store an array of tuples as defined here:
        - (`old_field_path`: str, `new_field_path`: str,
        `transform_func`: Optional[Callable[Any, Dict]->Any])
    """

    @staticmethod
    @abstractmethod
    def get_mapping() -> List[Mapping]:
        """
        Abstract static function containing the list of `Mapping`s, to be defined by the
        implementing class and is used by the `transform` function to transform raw data.

        Returns:
            List[Mapping]: List of `(old_field_path, new_field_path, transform_func, default_val)`
                NamedTuples
        """
        raise NotImplementedError()

    @classmethod
    def transform(cls, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Performs transformations on the input dictionary using the
        provided mappings in the `get_mapping` function.


        Args:
            data (Dict[Any, Any]): The original raw data object.

        Returns:
            Dict[Any, Any]: The transformed data object.

        Raise:
            TransformFuncError: Raised if the transform_func ecounters an error, e.g. TypeError
        """
        result = {}
        for (
            old_field_path,
            new_field_path,
            transform_func,
            default_val,
        ) in cls.get_mapping():
            if not objects.has(data, old_field_path):
                objects.set_(
                    result,
                    new_field_path,
                    default_val,
                )
                continue

            old_val = objects.get(data, old_field_path)

            try:
                new_val = transform_func(old_val, data) if transform_func else old_val
            except Exception as err:
                raise TransformFuncError(
                    f"The transform_func raised {err.__class__.__name__} when"
                    f" mapping ({old_field_path}:{old_val}) to ({new_field_path})"
                ) from err

            objects.set_(
                result,
                new_field_path,
                new_val,
            )
        return result
