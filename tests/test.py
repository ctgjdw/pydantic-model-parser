import unittest
from typing import List, Optional

from pydantic import BaseModel

from model_parser.custom_types import DefaultValFuncError
from model_parser import Mapping, BaseMapper, Parser, PydanticError, TransformFuncError


class User(BaseModel):
    id: int
    name: str
    first_name: Optional[str]
    tags: list


class Comment(BaseModel):
    id: int
    comment_str: Optional[str]
    user: User
    address_str: str
    comment_backup: Optional[str]


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
                lambda street, data: f"{street} {data.get('block_name', 'default')}"
                f" {data.get('unit_name', 'default')}",
            ),
            # user_first_name does not exist in input dict, defaults to None in new dict
            Mapping("user_first_name", "user.first_name"),
            # user_tags does not exist in input dict, use default_val instead in new dict
            Mapping("user_tags", "user.tags", default_val=[]),
            Mapping(
                "comment_id",
                "comment_id",
                default_val_func=lambda data: int(data.get("comment_id_str"))
                if data.get("comment_id_str")
                else None,
            ),
        ]


MAPPER = CommentMapper()
PARSER = Parser(Comment, CommentMapper)


def get_input():
    return {
        "id": 1,
        "comment_id_str": "1",
        "user_id": "2",
        "user_name": "bob",
        "street_name": "123 St",
        "block_name": "244",
        "unit_name": "10-123",
    }


def get_output():
    return {
        "id": 1,
        "comment_str": None,
        "user": {"id": 2, "name": "bob", "first_name": None, "tags": []},
        "address_str": "123 St 244 10-123",
        "comment_id": 1,
    }


class TestMapperTransformFunc(unittest.TestCase):
    def setUp(self):
        self.mapper = MAPPER
        self.input = get_input()
        self.output = get_output()

    def test_success(self):
        self.assertDictEqual(self.mapper.transform(self.input), self.output)

    def test_empty_input_dict_success(self):
        self.input = {}
        self.output = self.output = {
            "id": None,
            "comment_str": None,
            "user": {"id": None, "name": None, "first_name": None, "tags": []},
            "address_str": None,
            "comment_id": None,
        }
        self.assertDictEqual(self.mapper.transform(self.input), self.output)

    def test_transform_func_error(self):
        self.input["user_id"] = "1a"
        with self.assertRaises(TransformFuncError):
            self.mapper.transform(self.input)

    def test_default_func_error(self):
        self.input["comment_id_str"] = "1a"
        with self.assertRaises(DefaultValFuncError):
            self.mapper.transform(self.input)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = PARSER
        self.input = get_input()
        self.input_list = [get_input() for _ in range(3)]
        self.output = Comment.parse_obj(get_output())
        self.output_list = [Comment.parse_obj(get_output()) for _ in range(3)]

    def test_parse_single_dict_success(self):
        result = self.parser.parse(self.input)
        self.assertEqual(result, self.output)

    def test_parse_many_dicts_success(self):
        result = self.parser.parse(self.input_list)
        self.assertEqual(result, self.output_list)

    def test_parse_non_optional_field_pydantic_error(self):
        self.input["id"] = None
        with self.assertRaises(PydanticError):
            self.parser.parse(self.input)

    def test_parse_field_type_mismatch_pydantic_error(self):
        self.input["id"] = "id_str"
        with self.assertRaises(PydanticError):
            self.parser.parse(self.input)


if __name__ == "__main__":
    unittest.main()
