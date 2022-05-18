from typing import List
import datetime
from pydantic import BaseModel
from model_parser import Mapping, BaseMapper, Parser


class User(BaseModel):
    id: int
    name: str


class Comment(BaseModel):
    id: int
    comment_str: str
    user: User


class CommentMapper(BaseMapper):
    @staticmethod
    def get_mapping() -> List[Mapping]:
        return [
            ("id", "id", lambda x: int(x)),
            ("comment_str", "comment_str", None),
            ("user_name", "user.name", None),
            ("user_id", "user.id", None),
        ]


data = {
    "id": "1",
    "comment_str": "test",
    "user_id": 2,
    "user_name": "bob",
}
data_list = [data, data]
parser = Parser(Comment, CommentMapper)

# parse into a Comment entity
comment = parser.parse(data)

# parse into a list of Comment entities
comments = parser.parse(data_list)

print(comments)

