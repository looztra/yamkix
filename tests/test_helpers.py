"""Test helpers."""

from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, SingleQuotedScalarString

from yamkix.helpers import (
    convert_flow_to_block_style,
    convert_single_to_double_quotes,
    get_yamkix_version,
    remove_all_linebreaks,
    string_is_comment,
    strip_leading_double_space,
)


def test_remove_all_linebreaks() -> None:
    """Test remove_all_linebreaks.

    when there is a trailing linebreak
    """
    s_input = "yolo\n"
    sut = remove_all_linebreaks(s_input)
    assert sut == "yolo"


def test_remove_all_linebreaks_no_linebreak() -> None:
    """Test remove_all_linebreaks.

    when there is no trailing linebreak
    """
    s_input = "yolo"
    sut = remove_all_linebreaks(s_input)
    assert sut == "yolo"


def test_remove_all_linebreaks_more_than_one() -> None:
    """Test remove_all_linebreaks.

    when there is more than one linebreak
    """
    s_input = "line1\nline2\n"
    sut = remove_all_linebreaks(s_input)
    assert sut == "line1line2"


def test_string_is_comment() -> None:
    """Test string_is_comment.

    When it is a comment
    """
    s_input = "# I am a comment"
    assert string_is_comment(s_input)


def test_string_is_comment_when_not() -> None:
    """Test string_is_comment.

    When it is not a comment
    """
    s_input = "I am not a comment"
    assert not string_is_comment(s_input)


def test_string_is_comment_with_two_following_comment_tokens() -> None:
    """Test string_is_comment.

    When it is a comment with another #
    """
    s_input = "## I am a comment"
    assert string_is_comment(s_input)


def test_string_is_comment_with_two_comment_tokens() -> None:
    """Test string_is_comment.

    When it is a comment with another #
    """
    s_input = "# I am a comment #"
    assert string_is_comment(s_input)


def test_string_is_comment_when_not_because_not_leading() -> None:
    """Test string_is_comment.

    When it is not a comment
    """
    s_input = " # I am not a comment"
    assert not string_is_comment(s_input)


def test_string_is_comment_when_not_because_ending() -> None:
    """Test string_is_comment.

    When it is not a comment
    """
    s_input = "I am not a comment #"
    assert not string_is_comment(s_input)


def test_strip_leading_double_space() -> None:
    """Test strip_leading_double_space.

    when there are
    """
    stream = "  text1\n  text2"

    actual = strip_leading_double_space(stream)
    expected = "text1\ntext2"
    assert actual == expected


def test_strip_leading_double_space_mixed() -> None:
    """Test strip_leading_double_space.

    when there are but not everywhere
    """
    stream = "  text1\ntext2\n  text3\n"

    actual = strip_leading_double_space(stream)
    expected = "text1\ntext2\ntext3\n"
    assert actual == expected


def test_strip_leading_double_space_when_none() -> None:
    """Test strip_leading_double_space.

    when there are none
    """
    stream = "text1\ntext2\n"
    actual = strip_leading_double_space(stream)
    assert actual == stream


def test_get_yamkix_version() -> None:
    """Test get_yamkix_version.

    Ensures the function returns a valid version string.
    """
    version = get_yamkix_version()

    # Version should be a non-empty string
    assert isinstance(version, str)
    assert len(version) > 0


class TestConvertSingleToDoubleQuotes:
    """Test cases for convert_single_to_double_quotes function."""

    def test_convert_single_quoted_string_to_double_quoted(self) -> None:
        """Test converting a single quoted string to double quoted."""
        single_quoted = SingleQuotedScalarString("hello world")
        result = convert_single_to_double_quotes(single_quoted)

        assert isinstance(result, DoubleQuotedScalarString)
        assert str(result) == "hello world"

    def test_leave_double_quoted_string_unchanged(self) -> None:
        """Test that double quoted strings are left unchanged."""
        double_quoted = DoubleQuotedScalarString("hello world")
        result = convert_single_to_double_quotes(double_quoted)

        assert result is double_quoted
        assert isinstance(result, DoubleQuotedScalarString)
        assert str(result) == "hello world"

    def test_leave_regular_string_unchanged(self) -> None:
        """Test that regular strings are left unchanged."""
        regular_string = "hello world"
        result = convert_single_to_double_quotes(regular_string)

        assert result is regular_string
        assert result == "hello world"

    def test_leave_non_string_types_unchanged(self) -> None:
        """Test that non-string types are left unchanged."""
        test_cases = [
            42,
            3.14,
            True,
            False,
            None,
        ]

        for test_case in test_cases:
            result = convert_single_to_double_quotes(test_case)
            assert result is test_case

    def test_convert_dict_with_single_quoted_values(self) -> None:
        """Test converting single quoted strings in dictionary values."""
        input_dict = {
            "key1": SingleQuotedScalarString("value1"),
            "key2": "regular_value",
            "key3": SingleQuotedScalarString("value3"),
        }

        result = convert_single_to_double_quotes(input_dict)

        assert result is input_dict  # Should modify in place
        assert isinstance(result["key1"], DoubleQuotedScalarString)
        assert str(result["key1"]) == "value1"
        assert result["key2"] == "regular_value"
        assert isinstance(result["key3"], DoubleQuotedScalarString)
        assert str(result["key3"]) == "value3"

    def test_convert_list_with_single_quoted_values(self) -> None:
        """Test converting single quoted strings in list items."""
        test_number = 42
        input_list = [
            SingleQuotedScalarString("item1"),
            "regular_item",
            SingleQuotedScalarString("item3"),
            test_number,
        ]

        result = convert_single_to_double_quotes(input_list)

        assert result is input_list  # Should modify in place
        assert isinstance(result[0], DoubleQuotedScalarString)
        assert str(result[0]) == "item1"
        assert result[1] == "regular_item"
        assert isinstance(result[2], DoubleQuotedScalarString)
        assert str(result[2]) == "item3"
        assert result[3] == test_number

    def test_convert_nested_dict_structure(self) -> None:
        """Test converting single quoted strings in nested dictionary structure."""
        input_dict = {
            "level1": {
                "level2": {
                    "key": SingleQuotedScalarString("nested_value"),
                    "regular": "string",
                },
                "list": [SingleQuotedScalarString("list_item")],
            },
            "simple": SingleQuotedScalarString("simple_value"),
        }

        result = convert_single_to_double_quotes(input_dict)

        assert result is input_dict  # Should modify in place
        nested_value = result["level1"]["level2"]["key"]
        assert isinstance(nested_value, DoubleQuotedScalarString)
        assert str(nested_value) == "nested_value"

        list_item = result["level1"]["list"][0]
        assert isinstance(list_item, DoubleQuotedScalarString)
        assert str(list_item) == "list_item"

        simple_value = result["simple"]
        assert isinstance(simple_value, DoubleQuotedScalarString)
        assert str(simple_value) == "simple_value"

    def test_convert_nested_list_structure(self) -> None:
        """Test converting single quoted strings in nested list structure."""
        input_list = [
            [SingleQuotedScalarString("nested_item")],
            {"key": SingleQuotedScalarString("dict_in_list")},
            SingleQuotedScalarString("simple_item"),
        ]

        result = convert_single_to_double_quotes(input_list)

        assert result is input_list  # Should modify in place
        nested_item = result[0][0]
        assert isinstance(nested_item, DoubleQuotedScalarString)
        assert str(nested_item) == "nested_item"

        dict_value = result[1]["key"]
        assert isinstance(dict_value, DoubleQuotedScalarString)
        assert str(dict_value) == "dict_in_list"

        simple_item = result[2]
        assert isinstance(simple_item, DoubleQuotedScalarString)
        assert str(simple_item) == "simple_item"

    def test_convert_empty_structures(self) -> None:
        """Test converting empty dictionaries and lists."""
        empty_dict = {}
        empty_list = []

        result_dict = convert_single_to_double_quotes(empty_dict)
        result_list = convert_single_to_double_quotes(empty_list)

        assert result_dict is empty_dict
        assert result_dict == {}
        assert result_list is empty_list
        assert result_list == []

    def test_convert_complex_mixed_structure(self) -> None:
        """Test converting a complex mixed structure with various types."""
        timeout_value = 30
        complex_structure = {
            "users": [
                {
                    "name": SingleQuotedScalarString("John Doe"),
                    "email": "john@example.com",
                    "settings": {
                        "theme": SingleQuotedScalarString("dark"),
                        "notifications": True,
                        "timeout": timeout_value,
                    },
                },
                {
                    "name": SingleQuotedScalarString("Jane Smith"),
                    "tags": [
                        SingleQuotedScalarString("admin"),
                        "user",
                        SingleQuotedScalarString("active"),
                    ],
                },
            ],
            "config": {
                "version": SingleQuotedScalarString("1.0.0"),
                "debug": False,
            },
        }

        result = convert_single_to_double_quotes(complex_structure)

        # Check user names
        john_name = result["users"][0]["name"]
        assert isinstance(john_name, DoubleQuotedScalarString)
        assert str(john_name) == "John Doe"

        jane_name = result["users"][1]["name"]
        assert isinstance(jane_name, DoubleQuotedScalarString)
        assert str(jane_name) == "Jane Smith"

        # Check nested settings
        theme = result["users"][0]["settings"]["theme"]
        assert isinstance(theme, DoubleQuotedScalarString)
        assert str(theme) == "dark"

        # Check tags
        admin_tag = result["users"][1]["tags"][0]
        assert isinstance(admin_tag, DoubleQuotedScalarString)
        assert str(admin_tag) == "admin"

        active_tag = result["users"][1]["tags"][2]
        assert isinstance(active_tag, DoubleQuotedScalarString)
        assert str(active_tag) == "active"

        # Check config version
        version = result["config"]["version"]
        assert isinstance(version, DoubleQuotedScalarString)
        assert str(version) == "1.0.0"

        # Check that non-string values are unchanged
        assert result["users"][0]["email"] == "john@example.com"
        assert result["users"][0]["settings"]["notifications"] is True
        assert result["users"][0]["settings"]["timeout"] == timeout_value
        assert result["users"][1]["tags"][1] == "user"
        assert result["config"]["debug"] is False


def _load_yaml(text: str) -> Any:  # noqa: ANN401
    """Load YAML text using the round-trip loader."""
    yaml = YAML()
    return yaml.load(text)


class TestConvertFlowToBlockStyle:
    """Test cases for convert_flow_to_block_style function."""

    def test_flow_sequence_is_converted(self) -> None:
        """Test that a top-level flow sequence is converted to block style."""
        data = _load_yaml("a_list: [a, b, c]\n")
        assert data["a_list"].fa.flow_style() is True
        convert_flow_to_block_style(data)
        assert data["a_list"].fa.flow_style() is False

    def test_flow_mapping_is_converted(self) -> None:
        """Test that a top-level flow mapping is converted to block style."""
        data = _load_yaml("a_map: {first: yolo, second: foo}\n")
        assert data["a_map"].fa.flow_style() is True
        convert_flow_to_block_style(data)
        assert data["a_map"].fa.flow_style() is False

    def test_nested_flow_structures_are_converted(self) -> None:
        """Test that nested flow-style sequences and mappings are all converted."""
        data = _load_yaml("outer: {inner_list: [x, y], inner_map: {a: 1}}\n")
        assert data["outer"].fa.flow_style() is True
        convert_flow_to_block_style(data)
        assert data["outer"].fa.flow_style() is False
        assert data["outer"]["inner_list"].fa.flow_style() is False
        assert data["outer"]["inner_map"].fa.flow_style() is False

    def test_already_block_style_is_unchanged(self) -> None:
        """Test that block-style structures are unaffected."""
        data = _load_yaml("a_list:\n  - a\n  - b\n")
        assert data["a_list"].fa.flow_style() is False
        convert_flow_to_block_style(data)
        assert data["a_list"].fa.flow_style() is False

    def test_scalar_values_are_not_modified(self) -> None:
        """Test that scalar values pass through without error."""
        data = _load_yaml("key: value\n")
        convert_flow_to_block_style(data)
        assert data["key"] == "value"

    def test_mixed_document_converts_only_flow_parts(self) -> None:
        """Test that only flow-style parts of a mixed document are converted."""
        yaml_text = "block_list:\n  - a\n  - b\nflow_list: [x, y]\n"
        data = _load_yaml(yaml_text)
        assert data["block_list"].fa.flow_style() is False
        assert data["flow_list"].fa.flow_style() is True
        convert_flow_to_block_style(data)
        assert data["block_list"].fa.flow_style() is False
        assert data["flow_list"].fa.flow_style() is False
