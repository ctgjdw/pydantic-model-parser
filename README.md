# Pydantic Model Parser

A simple package to transform/map dictionaries, before parsing it into Pydantic.

## Requirements

- The models/entities should conform to `Pydantic's` Model specifications and should inherit the `pydantic.BaseModel` class.

## Installation

```bash
pip3 install pydantic-model-parser==3.0.*
```

## Usage

Firstly, define your entity using Pydantic's `BaseModel`.

```python
# comment.py
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    first_name: Optional[str]
    tags: list


class Comment(BaseModel):
    id: int
    comment_str: str
    user: User
    address_str: str
    comment_backup: Optional[str]
```

Next, define the `Mapper`. The mapper can be used to **rearrange** dictionary keys and **perform** transformations on the values. The mapper is a strict whitelist of **wanted** fields. Any fields not defined in the mapper will be **dropped** from the output model.

The Mapping args are as follows:

- (`old_field_path`: str, `new_field_path`: str, `transform_func`: Optional[Callable] = None, `default_val`: [None | Dict | List] = None, `default_val_func`: Optional[Callable])
- `transform_func` (Optional) of `None` maps the value as per the original value
- `transform_func` of `lambda x,_: x * 2` maps the value as double of the original value
- `transform_func` of `lambda x,y: x + y.field_name` maps the value to `x + y.field_name`, where y is the original data dictionary
- `default_val` (Optional) is used if `old_field_path` **does not exist** in the input dict as a key and `default_val_func` is not null
- `default_val_func` (Optional) is used if `old_field_path` **does not exist** in the input dict as a key. This function takes in the original data dictionary as an arguement for inserting old data fields as defaults during runtime.
- `old_field_path`'s value is mapped to the position defined in `new_field_path` in the output dictionary and subsequently parsed into the `BaseModel`
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
from typings import List
from model_parser import Mapping, BaseMapper

class CommentMapper(BaseMapper):
    @staticmethod
    def get_mapping() -> List[Mapping]:
        return [
            # Maps the val of id to id
            Mapping("id", "id"),
            # Maps the val of comment_str to comment_str
            Mapping("comment_str", "comment_str"),
            # Rename key from user_name to user.name, where the `.` indicates a level of nesting
            Mapping("user_name", "user.name"),
            # Using transform_func to transform value and insert to new dict
            Mapping("user_id", "user.id", lambda id_str, _: int(id_str)),
            # Using transform_func to transform value using an existing value from the original dict
            ## This is prone to more errors, please catch and handle TransformFuncError
            Mapping(
                "street_name",
                "address_str",
                lambda street, data: f"{street} {data.get('block_name', 'default')} {data.get('unit_name', 'default')}",
            ),
            # user_first_name does not exist in input dict, defaults to None in new dict
            Mapping("user_first_name", "user.first_name"),
            # user_tags does not exist in input dict, use default_val instead in new dict
            Mapping("user_tags", "user.tags", default_val=[]),
            Mapping(
                "comment_backup",
                "comment_backup",
                default_val_func=lambda data: data.get("comment_str"),
            ),
        ]
```
### Transform data dict using mappings
To **transform** a raw dict to a new format according to the mappings:

```python
# main.py
from comment import CommentMapper

data = {
        "id": 1,
        "comment_str": "HelloWorld",
        "user_id": "2",
        "user_name": "bob",
        "street_name": "123 St",
        "block_name": "244",
        "unit_name": "10-123"
    }
# transform dict to new_dict (after mapping)
try:
  MAPPED_COMMENT_DICT = CommentMapper.transform(data)
  print(MAPPED_COMMENT_DICT)
except TransformFuncError as err:
    print(err)
except DefaultValFuncError as err:
    print(err)
```

Output:
> `{'id': 1, 'comment_str': 'HelloWorld', 'user': {'name': 'bob', 'id': 2, 'first_name': None, 'tags': []}, 'address_str': '123 St 244 10-123', 'comment_backup': 'HelloWorld'}`

### Parse data dict to pydantic object
To **parse** and **transform** a raw dict to a pydantic object:

```python
# main.py
from comment import Comment, CommentMapper
from model_parser import Parser

data = {
    "id": 1,
    "comment_str": "HelloWorld",
    "user_id": "2",
    "user_name": "bob",
    "street_name": "123 St",
    "block_name": "244",
    "unit_name": "10-123",
}
data_list = [data, data]
parser = Parser(Comment, CommentMapper)

try:
    COMMENT = parser.parse(data)
except TransformFuncError:
    print("Error applying transform_func!")
except DefaultValFuncError:
    print("Error applying default_val_func!")
except PydanticError:
    print("Validation Error when parsing into Pydantic")

# parse into a list of Comment entities
try:
    COMMENTS = parser.parse(data_list)
except TransformFuncError:
    print("Error applying transform_func!")
except DefaultValFuncError:
    print("Error applying default_val_func!")
except PydanticError:
    print("Validation Error when parsing into Pydantic")

print(COMMENT)
```

Output:
> `id=1 comment_str='HelloWorld' user=User(id=2, name='bob', first_name=None, tags=[]) address_str='123 St 244 10-123' comment_backup='HelloWorld'`