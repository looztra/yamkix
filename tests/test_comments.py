"""Test the comments management."""

import pytest
from pytest_mock import MockerFixture
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

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


@pytest.mark.xfail(
    strict=True,
    reason="CMT-R005: align_one reads the map comment slot [2]; list items keep their EOL comment in slot [0]",
)
def test_align_comments_with_sequence() -> None:
    """Test align_comments aligns the EOL comments of a real CommentedSeq on its rightmost comment."""
    yaml = YAML()
    code = yaml.load("items:\n- a # c1\n- longer_value # c2\n")
    items = code["items"]

    align_comments(code)

    assert items.ca.items[0][0].column == items.ca.items[1][0].column


def test_align_comments_with_some_null_comments(mocker: MockerFixture) -> None:
    """Test align_comments when some comments have comment[2] as None.

    This covers line 91 (the guard 'if comment[2] is not None').
    """
    comment_mock_1 = mocker.Mock(column=3)
    comment_mock_2 = mocker.Mock(column=5)

    mock_seq_ca = mocker.Mock(
        spec=CommentedSeq,
        items={
            0: [None, None, comment_mock_1],
            1: [None, None, comment_mock_2],
            2: [None, None, None],  # comment[2] is None - exercises line 91
        },
    )
    mock_seq = mocker.Mock(spec=CommentedSeq, ca=mock_seq_ca)
    mock_seq.__iter__ = mocker.Mock(return_value=iter([]))

    align_comments(mock_seq)

    assert comment_mock_1.column == 5
    assert comment_mock_2.column == 5
