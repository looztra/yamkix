"""Sandbox for aligning comments.

Original source code from https://stackoverflow.com/questions/71332643/how-do-i-align-the-eol-comments-in-ruamel-yaml-so-that-they-are-all-in-the-same
"""

import io
import sys
from pathlib import Path

from rich import print as rprint
from ruamel.yaml import YAML, CommentedMap

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
top = CommentedMap()
top["sub_key1"] = data = CommentedMap()

data["a"] = 1
data["b"] = "asdf"
data["c"] = 3.3333
data.yaml_add_eol_comment("comment 1", "a")
data.yaml_add_eol_comment("comment 2", "b")
data.yaml_add_eol_comment("comment 3", "c")

top["sub_key2"] = data = CommentedMap()

data["a"] = "long text"
data["b"] = "an even longer text"
data.yaml_add_eol_comment("comment 4\n# that's all folks", "a")
data.yaml_add_eol_comment("comment 5", "b")

buf = io.BytesIO()
yaml.dump(top, buf)

# top = yaml.load(buf.getvalue())  # noqa: ERA001
with Path("generated/test-assets/source/with-comments-to-align.yml").open(encoding="utf-8") as f:
    top = yaml.load(f.read())


def align_comments_anthon(d: CommentedMap, extra_indent: int = 0) -> None:  # noqa: D103
    def align_one(d: CommentedMap, extra_indent: int = 0) -> None:
        rprint(f"{d=}")
        index_in_comment = 2
        if isinstance(d, list):
            index_in_comment = 0
        comments = d.ca.items.values()
        if not comments:
            rprint("No comments to align")
            return
        max_column_index = -1
        for comment in comments:
            rprint(f"{comment=}")
            max_column_index = max(max_column_index, comment[index_in_comment].column)
        rprint(f"Max column index: {max_column_index}")
        for comment in comments:
            comment[index_in_comment].column = max_column_index + extra_indent

    if isinstance(d, dict):
        align_one(d, extra_indent=extra_indent)
        for val in d.values():
            align_comments_anthon(val, extra_indent=extra_indent)
    elif isinstance(d, list):
        align_one(d, extra_indent=extra_indent)
        for elem in d:
            align_comments_anthon(elem, extra_indent=extra_indent)


def align_comments_spaceman_spiff(d: CommentedMap, extra_indent: int = 0) -> None:  # noqa: D103
    is_dict = isinstance(d, dict)
    if not is_dict and not isinstance(d, list):
        return

    comments = d.ca.items.values()
    if comments:
        max_col = max((x[2].column for x in comments), default=0)
        for comment in comments:
            comment[2].column = max_col + extra_indent

    for element in d.values() if is_dict else d:
        align_comments_spaceman_spiff(element, extra_indent=extra_indent)
    return


align_comments_anthon(top, extra_indent=1)
rprint("==result==")
yaml.dump(top, sys.stdout)
