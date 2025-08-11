"""Tests the args parsing."""

from yamkix.args import get_override_or_default


class TestArgs:
    """Provide unit tests for the args package."""

    def test_get_override_or_default_when_key_doesnt_exist(self) -> None:
        """Test get_override_or_default when key doesn't exist."""
        sut = {}
        key = "any"
        default_value = "yolo"
        result = get_override_or_default(sut, key, default_value)
        assert result == default_value

    def test_get_override_or_default_when_key_exists(self) -> None:
        """Test get_override_or_default when key exists."""
        sut = {}
        key = "i_m_the_one"
        value_for_key = "yamkix_rulez"
        default_value = "yolo"
        sut[key] = value_for_key
        result = get_override_or_default(sut, key, default_value)
        assert result == value_for_key

    def test_get_override_or_default_when_override_is_none(self) -> None:
        """Test get_override_or_default when override is none."""
        sut = None
        key = "any"
        default_value = "yolo"
        result = get_override_or_default(sut, key, default_value)
        assert result == default_value
