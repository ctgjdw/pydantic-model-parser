from typing import Any, Callable, Tuple, Optional

NewField = str
OldField = str
TransformFunc = Callable[[Any], Any]
Mapping = Tuple[NewField, OldField, Optional[TransformFunc]]


class MappingError(Exception):
    pass


class TransformFuncError(Exception):
    pass
