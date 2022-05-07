# Pydantic Model Parser

A simple package to transform/map dictionaries, before parsing it into Pydantic.

## Requirements

- The models/entities should conform to `Pydantic's` Model specifications and should inherit the `pydantic.BaseModel`.

## Installation

```bash
pip3 install pydantic-model-parser
```

## Usage

Firstly, define your entity using Pydantic's `BaseModel`.

```python
# comment.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str


class Comment(BaseModel):
    id: int
    comment_str: str
    user: User
```

Next, define the `Mapper`. The mapper can be used to **rearrange** dictionary keys and **perform** transformations on the values.

The tuples definitions are as follows:

- (`old_field_path`: str, `new_field_path`: str, `transform_func`: Optional[Callable])
- `transform_func` of `None` maps the value as per the original value
- `transform_func` of `lambda x: x * 2` maps the value as double of the original value
- `old_field_path`'s value is placed in `new_field_path` in the new dictionary and subsequently parsed into the `BaseModel`
  - The `.` in the path delimits the nested levels in the dictionaries. e.g. `user.id` refers to:

```json
{
    "user": {
        "id": 1
    }
}
```

Defining a Mapper:

```python
# comment.py
from model_parser.custom_types import Mapping
from model_parser.mapper import BaseMapper

class CommentMapper(BaseMapper):
    @staticmethod
    def get_mapping() -> List[Mapping]:
        return [
            ('id', 'id', None),
            ('comment_str', 'comment_str', None),
            ('user_name', 'user.name', None),
            ('user_id', 'user.id', None)
        ]
```

Lastly, to **parse** objects:

```python
# main.py
from comment import Comment, CommentMapper

data = {
        "id": 1,
        "comment_str": "HelloWorld",
        "user_id": 2,
        "user_name": "bob"
    }
data_list = [data, data]
parser = Parser(Comment, CommentMapper)

# parse into a Comment entity
comment = parser.parse(data)

# parse into a list of Comment entities
comments = parser.parse(data_list)
```
