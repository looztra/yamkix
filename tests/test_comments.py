"""Test the comments management."""

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


def test_align_comments_with_no_comments(mocker: MockerFixture) -> None:
    """Test align_comments when there are no comments in the data structure.

    This covers line 91 (the early return when comments is empty).
    """
    mock_ca = mocker.Mock(spec=CommentedMap, items={})
    mock_data = mocker.Mock(spec=CommentedMap, ca=mock_ca)
    mock_data.values.return_value = []
    align_comments(mock_data)


def test_align_comments_with_sequence(mocker: MockerFixture) -> None:
    """Test align_comments with a CommentedSeq containing comments.

    This covers lines 102-104 (the sequence handling branch).
    """
    comment_mock_1 = mocker.Mock(column=3)
    comment_mock_2 = mocker.Mock(column=5)
    comment_mock_3 = mocker.Mock(column=4)

    mock_seq_ca = mocker.Mock(
        spec=CommentedSeq,
        items={
            0: [None, None, comment_mock_1],
            1: [None, None, comment_mock_2],
            2: [None, None, comment_mock_3],
        },
    )
    mock_inner_ca = mocker.Mock(spec=CommentedMap, items={})
    mock_inner_data = mocker.Mock(spec=CommentedMap, ca=mock_inner_ca)
    mock_inner_data.values.return_value = []

    mock_seq = mocker.Mock(spec=CommentedSeq, ca=mock_seq_ca)
    mock_seq.__iter__ = mocker.Mock(return_value=iter([mock_inner_data]))

    align_comments(mock_seq)

    assert comment_mock_1.column == 5
    assert comment_mock_2.column == 5
    assert comment_mock_3.column == 5
