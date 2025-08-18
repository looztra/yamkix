"""Provide non regression tests."""

import filecmp
from pathlib import Path

import pytest
from typer.testing import CliRunner

from yamkix._cli import app

runner = CliRunner()


@pytest.mark.non_regression
class TestNonRegression:
    """Provide non-regression tests using the cli."""

    @pytest.mark.parametrize(
        ("test_case", "config_name", "cli_args"),
        [
            pytest.param(
                "dash-at-col0-1", "no-dash-inwards", ["--no-dash-inwards"], id="dash_at_col0_1_no_dash_inwards"
            ),
            pytest.param(
                "dash-at-col2-1", "no-dash-inwards", ["--no-dash-inwards"], id="dash_at_col2_1_no_dash_inwards"
            ),
            pytest.param("multi-doc-1", "no-dash-inwards", ["--no-dash-inwards"], id="multi_doc_1_no_dash_inwards"),
            pytest.param("dash-at-col0-1", "set-dash-inwards", [], id="dash_at_col0_1_set_dash_inwards"),
            pytest.param("dash-at-col2-1", "set-dash-inwards", [], id="dash_at_col2_1_set_dash_inwards"),
            pytest.param(
                "lists-and-maps-json-style", "set-dash-inwards", [], id="lists_and_maps_json_style_set_dash_inwards"
            ),
            pytest.param("multi-doc-1", "set-dash-inwards", [], id="multi_doc_1_set_dash_inwards"),
            pytest.param("no-start-no-end", "default", [], id="no_start_no_end_default"),
            pytest.param(
                "no-start-no-end",
                "no-explicit-start",
                ["--no-explicit-start"],
                id="no_start_no_end_no_explicit_start",
            ),
            pytest.param(
                "no-start-no-end",
                "set-explicit-end",
                ["--explicit-end"],
                id="no_start_no_end_set_explicit_end",
            ),
            pytest.param(
                "no-start-no-end",
                "no-quotes-preserved",
                ["--no-quotes-preserved"],
                id="no_start_no_end_no_quotes_preserved",
            ),
            pytest.param(
                "issue-11-bad-indent",
                "spaces-before-comment-2--no-dash-inwards",
                ["--spaces-before-comment", "2", "--no-dash-inwards"],
                id="issue_11_bad_indent_spaces_before_comment_2_no_dash_inwards",
            ),
            pytest.param(
                "issue-11",
                "spaces-before-comment-2--no-dash-inwards",
                ["--spaces-before-comment", "2", "--no-dash-inwards"],
                id="issue_11_spaces_before_comment_2_no_dash_inwards",
            ),
            pytest.param(
                "issue-29",
                "spaces-before-comment-1--no-dash-inwards",
                ["--spaces-before-comment", "1", "--no-dash-inwards"],
                id="issue_29_spaces_before_comment_1_no_dash_inwards",
            ),
            pytest.param(
                "issue-29",
                "spaces-before-comment-2--no-dash-inwards",
                ["--spaces-before-comment", "2", "--no-dash-inwards"],
                id="issue_29_spaces_before_comment_2_no_dash_inwards",
            ),
            pytest.param(
                "issue-11-bad-indent",
                "spaces-before-comment-2",
                ["--spaces-before-comment", "2"],
                id="issue_11_bad_indent_spaces_before_comment_2",
            ),
            pytest.param(
                "issue-11",
                "spaces-before-comment-2",
                ["--spaces-before-comment", "2"],
                id="issue_11_spaces_before_comment_2",
            ),
            pytest.param(
                "issue-11",
                "spaces-before-comment-1",
                ["--spaces-before-comment", "1"],
                id="issue_11_spaces_before_comment_1",
            ),
            pytest.param(
                "issue-11",
                "spaces-before-comment-0",
                ["--spaces-before-comment", "0"],
                id="issue_11_spaces_before_comment_0",
            ),
            pytest.param(
                "issue-11-ruamel-318",
                "spaces-before-comment-2",
                ["--spaces-before-comment", "2"],
                id="issue_11_ruamel_318_spaces_before_comment_2",
            ),
            pytest.param(
                "issue-11-ruamel-318",
                "spaces-before-comment-1",
                ["--spaces-before-comment", "1"],
                id="issue_11_ruamel_318_spaces_before_comment_1",
            ),
            pytest.param(
                "issue-11-ruamel-338",
                "spaces-before-comment-2",
                ["--spaces-before-comment", "2"],
                id="issue_11_ruamel_318_spaces_before_comment_2",
            ),
            pytest.param(
                "issue-11-ruamel-338",
                "spaces-before-comment-1",
                ["--spaces-before-comment", "1"],
                id="issue_11_ruamel_338_spaces_before_comment_1",
            ),
            pytest.param(
                "k8s-deployment-with-comments-1",
                "spaces-before-comment-1",
                ["--spaces-before-comment", "1"],
                id="k8s_deployment_with_comments_1_spaces_before_comment_1",
            ),
            pytest.param(
                "k8s-deployment-with-comments-shifted-1",
                "spaces-before-comment-1",
                ["--spaces-before-comment", "1"],
                id="k8s_deployment_with_comments_shifted_1_spaces_before_comment_1",
            ),
            pytest.param(
                "issue-29",
                "spaces-before-comment-1",
                ["--spaces-before-comment", "1"],
                id="issue_29_spaces_before_comment_1",
            ),
            pytest.param(
                "issue-29",
                "spaces-before-comment-2",
                ["--spaces-before-comment", "2"],
                id="issue_29_spaces_before_comment_2",
            ),
        ],
    )
    def test_config(
        self, test_case: str, config_name: str, cli_args: list[str], shared_datadir: Path, tmp_path: Path
    ) -> None:
        """Test the --no-dash-inwards option with a specific input file."""
        input_file = shared_datadir / "source" / f"{test_case}.yml"
        actual_output_file = tmp_path / "actual" / f"{test_case}.yml"
        actual_output_file.parent.mkdir(parents=True, exist_ok=True)
        expected_output_file = shared_datadir / "expected" / f"{test_case}--{config_name}.yml"
        base_cli_args = ["--input", str(input_file), "--output", str(actual_output_file)]
        base_cli_args.extend(cli_args)
        result = runner.invoke(app, base_cli_args)
        assert result.exit_code == 0
        assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)
