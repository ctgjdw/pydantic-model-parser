from typing import List

from pydantic import BaseModel

from base_parser import BaseParser
from custom_types import Mapping
from mapper import BaseMapper


class User(BaseModel):
    id: int
    name: str


class Tweet(BaseModel):
    id: int
    tweet: str
    user: User

class TweetMapper(BaseMapper):
    @staticmethod
    def get_mapping() -> List[Mapping]:
        return [
            ('id', 'id', None),
            ('tweet', 'tweet', None),
            ('user.name', 'user_name', None),
            ('user.id', 'user_id', None)
        ]
