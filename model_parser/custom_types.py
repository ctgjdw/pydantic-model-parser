from typing import Any, Callable, NamedTuple, Optional, Union, Dict, List


class Mapping(NamedTuple):
    """
    A `NamedTuple` that is used to map and transform (key, value)
    pairs between the input dict and the output dict.
    `Mapping` is also able to apply transformations
    via transform_func to the value prior
    to mapping. The original data dictionary is exposed as
    the 2nd positional argument in the transform_func to
    allow transformations during runtime

    Args:
        old_field_path (str): The path to the position of the key in the input dict,
            the level of nesting is delimited by `.`
        new_field_path (str): The path to the position of the key in the output dict,
            the level of nesting is delimited by `.`
        transform_func ((Any, Dict[Any,Any]) -> Any): The function to apply to the old_val prior
            to mapping the value to
            the output dict. Takes in the original data dictionary as a 2nd argument
            Defaults to `None`
        default_val (None | Dict | List): The default value to apply if the old_field_path
            is not present in the input dict. Defaults to `None`
    """

    old_field_path: str
    new_field_path: str
    transform_func: Optional[Callable[[Any, Dict[Any, Any]], Any]] = None
    default_val: Union[None, Dict, List] = None


class TransformFuncError(Exception):
    def __str__(self) -> str:
        return f"{self.args[0]}\n--CAUSE--\n{self.__cause__.__str__()}"


class PydanticError(Exception):
    def __str__(self) -> str:
        return f"{self.args[0]}\n--CAUSE--\n{self.__cause__.__str__()}"
