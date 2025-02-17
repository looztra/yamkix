"""Test the comments management."""

import unittest
from types import SimpleNamespace

from ruamel.yaml import YAML

from yamkix.comments import fix_for_issue29


class TestComments(unittest.TestCase):
    """Provide unit tests for the comments package."""

    def test_fix_for_issue29_when_not_none(self) -> None:
        """Test fix_for_issue29.

        When the data.ca.items[key][3] is not None
        and hence needs to be changed
        """
        sut_key = "sut"
        items = {"key1": 0, sut_key: [0, 1, 2, 3]}
        sut_ca = SimpleNamespace(items=items)
        sut_data = SimpleNamespace(dont="care", ca=sut_ca)

        assert sut_data.ca.items[sut_key][3] is not None
        fix_for_issue29(sut_data, sut_key)
        assert sut_data.ca.items[sut_key][3] is None

    def test_fix_for_issue29_when_none(self) -> None:
        """Test fix_for_issue29.

        When the data.ca.items[key][3] is None
        and hence doesn't need to be changed
        """
        sut_key = "sut"
        items = {"key1": 0, sut_key: [0, 1, 2, None]}
        sut_ca = SimpleNamespace(items=items)
        sut_data = SimpleNamespace(dont="care", ca=sut_ca)

        assert sut_data.ca.items[sut_key][3] is None
        fix_for_issue29(sut_data, sut_key)
        assert sut_data.ca.items[sut_key][3] is None

    def test_yamkix_add_eol_comment(self) -> None:
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
