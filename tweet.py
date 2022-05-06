from pydantic import BaseModel
from base_parser import BaseParser


class User(BaseModel):
    id: int
    name: str


class Tweet(BaseModel):
    id: int
    tweet: str
    user: User


class TweetParser(BaseParser):
    _mappers = [
        ('id', 'id', None),
        ('tweet', 'tweet', None),
        ('user.name', 'user_name', None),
        ('user.id', 'user_id', None)
    ]

    def __init__(self):
        super().__init__(Tweet, self._mappers)
