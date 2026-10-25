"""Test the comments management."""

from io import StringIO

from pytest_mock import MockerFixture
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from yamkix.comments import align_comments, fix_for_issue29


def test_fix_for_issue29_when_not_none(mocker: MockerFixture) -> None:
    """Test fix_for_issue29.

    When the data.ca.items[key][3] is not None
    and hence needs to be changed
    """
    sut_key = "sut"
    items = {"key1": 0, sut_key: [0, 1, 2, 3]}
    sut_ca = mocker.Mock(spec=CommentedMap, items=items)
    sut_data = mocker.Mock(spec=CommentedMap, dont="care", ca=sut_ca)
    assert sut_data.ca.items[sut_key][3] is not None
    fix_for_issue29(sut_data, sut_key)
    assert sut_data.ca.items[sut_key][3] is None


def test_fix_for_issue29_when_none(mocker: MockerFixture) -> None:
    """Test fix_for_issue29.

    When the data.ca.items[key][3] is None
    and hence doesn't need to be changed
    """
    sut_key = "sut"
    items = {"key1": 0, sut_key: [0, 1, 2, None]}
    sut_ca = mocker.Mock(spec=CommentedMap, items=items)
    sut_data = mocker.Mock(spec=CommentedMap, dont="care", ca=sut_ca)
    assert sut_data.ca.items[sut_key][3] is None
    fix_for_issue29(sut_data, sut_key)
    assert sut_data.ca.items[sut_key][3] is None


def test_yamkix_add_eol_comment() -> None:
    """Test yamkix_add_eol_comment."""
    inp = """\
    # example
    name:
    # details
    family: Smith   # very common
    given: Alice    # one of the siblings
    """
    yaml = YAML()
    code = yaml.load(inp)
    assert code["family"] == "Smith"


def test_align_comments_with_no_comments() -> None:
    """Test align_comments when there are no comments in the data structure.

    This covers the early return when ca.items is empty (line 88).
    """
    yaml = YAML()
    code = yaml.load("key: value")
    assert code.ca.items == {}
    align_comments(code)


def test_align_comments_with_sequence() -> None:
    """Test align_comments aligns the EOL comments of a list on its rightmost comment, skipping uncommented items."""
    yaml = YAML()
    code = yaml.load("items:\n- a # c1\n- longer_value # c2\n- b\n")

    align_comments(code)

    output = StringIO()
    yaml.dump(code, output)
    assert output.getvalue() == "items:\n- a            # c1\n- longer_value # c2\n- b\n"
