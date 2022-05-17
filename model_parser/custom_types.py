from typing import Any, Callable, Dict, Tuple, Optional

NewField = str
OldField = str
Transformer = Callable[[Any], Any]
Mapping = Tuple[NewField, OldField, Optional[Transformer]]
JsonObject = Dict[Any, Any]


class MappingError(Exception):
    pass


class TransformFuncError(Exception):
    pass
