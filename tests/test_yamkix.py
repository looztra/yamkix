"""Provide tests for the yamkix module."""

from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from yamkix.config import YamkixInputOutputConfig, get_yamkix_config_from_default
from yamkix.errors import InvalidYamlContentError
from yamkix.yamkix import round_trip_and_format


class TestRoundTripAndFormat:
    """Provide tests for the round_trip_and_format function."""

    def test_when_parser_error(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test that round_trip_and_format raises InvalidYamlContentError on ParserError."""
        # GIVEN
        mock_yamkix_dump_all = mocker.patch("yamkix.yamkix.yamkix_dump_all")
        config = get_yamkix_config_from_default(
            io_config=YamkixInputOutputConfig(input=str(shared_datadir / "malformed-yaml-file.yml"), output=None)
        )

        # WHEN / THEN
        with pytest.raises(InvalidYamlContentError):
            round_trip_and_format(config)
        mock_yamkix_dump_all.assert_not_called()
