"""Test the comments management."""

from pytest_mock import MockerFixture
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from yamkix.comments import fix_for_issue29


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
