from typing import List, Union, overload, Dict, Any, Type

from pydantic import BaseModel, ValidationError

from model_parser.mapper import BaseMapper
from model_parser.custom_types import PydanticError


class Parser:  # pylint: disable=too-few-public-methods
    """
    The Parser takes in a Pydantic `BaseModel` and a `model_parser.BaseMapper` to
    perform transformations and parse the object into the defined entity.

    Attributes:

        _model BaseModel: The Pydantic Model

        _mapper BaseMapper: The Mapper Class defined using model_parser.mapper.BaseMapper
    """

    def __init__(self, entity_model: Type[BaseModel], mapper: Type[BaseMapper]) -> None:
        self._model = entity_model
        self._mapper = mapper

    @overload
    def parse(self, data: Dict[Any, Any]) -> BaseModel:
        ...

    @overload
    def parse(self, data: List[Dict[Any, Any]]) -> List[BaseModel]:
        ...

    def parse(
        self, data: Union[Dict[Any, Any], List[Dict[Any, Any]]]
    ) -> Union[BaseModel, List[BaseModel]]:
        """
        The parse function takes in either [dict | list[dict]], performs the
        transformations as defined in the _mapper attribute and parses into
        the _model as a Pydantic entity

        Args:
            data (Union[Dict[Any, Any], List[Dict[Any, Any]]]): The raw data to transform and parse

        Returns:
            Union[BaseModel, List[BaseModel]]: The `Pydantic` entities
                                        as defined by  the _model attr

        Raise:
            PydanticError: Raised if there is a Validation Error
                        after parsing into the `Pydantic` Model. e.g. Invalid type-casting.
            TransformFuncError: Raised if the transform_func ecounters an error, e.g. TypeError
            DefaultValFuncError: Raised if the default_val_func ecounters an error, e.g. KeyError
        """
        if isinstance(data, dict):
            parsed = self._mapper.transform(data)
            try:
                return self._model.parse_obj(parsed)
            except ValidationError as err:
                raise PydanticError(
                    f"Validation Error: Unable to parse entity - {parsed}"
                ) from err

        parsed_list = [self._mapper.transform(item) for item in data]

        result = []
        for item in parsed_list:
            try:
                result.append(self._model.parse_obj(item))
            except ValidationError as err:
                raise PydanticError(
                    f"Validation Error: Unable to parse entity - {item}"
                ) from err
        return result
