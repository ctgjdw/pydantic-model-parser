from typing import List, Optional

from pydantic import BaseModel
from model_parser import Mapping, BaseMapper, Parser, PydanticError, TransformFuncError


class User(BaseModel):
    id: int
    name: str
    first_name: Optional[str]
    tags: list


class Comment(BaseModel):
    id: int
    comment_str: str
    user: User


class CommentMapper(BaseMapper):
    @staticmethod
    def get_mapping() -> List[Mapping]:
        return [
            Mapping("id", "id"),
            # Maps the val of comment_str to comment_str
            Mapping("comment_str", "comment_str"),
            # Rename key from user_name to user.name, where the `.` indicates a level of nesting
            Mapping("user_name", "user.name"),
            # Using transform_func to transform value and insert to new dict
            Mapping(
                "user_id",
                "user.id",
                lambda id_str: int(id_str) * 2,
            ),
            # user_first_name does not exist in input dict, defaults to None in new dict
            Mapping("user_first_name", "user.first_name"),
            # user_tags does not exist in input dict, use default_val instead in new dict
            Mapping("user_tags", "user.tags", default_val=[]),
        ]


data = {"id": 1, "comment_str": "HelloWorld", "user_id": "2", "user_name": "bob"}
data_list = [data, data]
parser = Parser(Comment, CommentMapper)

# transform dict to new_dict (after mapping)
MAPPED_COMMENT_DICT = CommentMapper.transform(data)

# parse into a Comment entity
try:
    COMMENT = parser.parse(data)
except TransformFuncError:
    print("Error applying transform_func!")
except PydanticError:
    print("Validation Error when parsing into Pydantic")

# parse into a list of Comment entities
try:
    COMMENTS = parser.parse(data_list)
except TransformFuncError:
    print("Error applying transform_func!")
except PydanticError:
    print("Validation Error when parsing into Pydantic")

print(MAPPED_COMMENT_DICT)
print(COMMENT)
