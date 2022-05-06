from typing import Any, Callable, Tuple, Optional

NewField = str
OldField = str
Transformer = Callable[[Any], Any]
Mapping = Tuple[NewField, OldField, Optional[Transformer]]