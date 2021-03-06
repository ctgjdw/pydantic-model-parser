from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable, Optional

from pydash import objects

from model_parser.custom_types import DefaultValFuncError, Mapping, TransformFuncError


class BaseMapper(ABC):
    """
    An abstract base class that should be extended and implemented
    by an EntityMapper class. The class stores the mappings in the `get_mapping`
    function.

    The `get_mapping` function will store an array of NamedTuples as defined here:
        - (`old_field_path`: str, `new_field_path`: str,
        `transform_func`: Optional[Callable[[Any,Dict], Any]], `default_val`: [None|Dict|List]
        , `default_val_func`: Optional[Callable])
    """

    @staticmethod
    @abstractmethod
    def get_mapping() -> List[Mapping]:
        """
        Abstract static function containing the list of `Mapping`s, to be defined by the
        implementing class and is used by the `transform` function to transform raw data.

        Returns:
            List[Mapping]: List of `(old_field_path, new_field_path, transform_func,
                default_val, default_val_func)` NamedTuples
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
            DefaultValFuncError: Raised if the default_val_func encounters an error, e.g. KeyError
        """
        result = {}
        for (
            old_field_path,
            new_field_path,
            transform_func,
            default_val,
            default_val_func,
        ) in cls.get_mapping():
            old_val = objects.get(data, old_field_path, default=None)
            if old_val is None:
                resolved_default_val = cls.__get_def_val(
                    data, default_val, default_val_func
                )
                objects.set_(
                    result,
                    new_field_path,
                    resolved_default_val,
                )
                continue

            objects.set_(
                result,
                new_field_path,
                cls.__get_new_val(
                    data, old_val, transform_func, old_field_path, new_field_path
                ),
            )
        return result

    @staticmethod
    def __get_def_val(
        old_dict: Dict[Any, Any],
        default_val: Any,
        default_val_func: Optional[Callable[[Dict[Any, Any]], Any]],
    ):
        try:
            return default_val if not default_val_func else default_val_func(old_dict)
        except Exception as err:
            raise DefaultValFuncError(
                f"The default_val_func raised {err.__class__.__name__}"
            ) from err

    @staticmethod
    def __get_new_val(
        old_dict: Dict[Any, Any],
        old_val: Any,
        transform_func: Optional[Callable[[Any, Dict[Any, Any]], Any]],
        old_field_path: str,
        new_field_path: str,
    ):
        try:
            return transform_func(old_val, old_dict) if transform_func else old_val
        except Exception as err:
            raise TransformFuncError(
                f"The transform_func raised {err.__class__.__name__} when"
                f" mapping ({old_field_path}:{old_val}) to ({new_field_path})"
            ) from err
