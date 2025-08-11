"""Play with comments."""

import sys

import ruamel.yaml
from rich import print as pprint
from ruamel.yaml.comments import CommentedBase, CommentedMap, NotNone
from ruamel.yaml.error import CommentMark
from ruamel.yaml.tokens import CommentToken

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
inp = """\
---
list-of-maps:
  - part_no:   A4786 # comment 1
    part_henon: mouhaha    # you're not funny
  - part_yes: A21 # also a comment here
    part_iculier: partenaire # I don't always understand how it works
    part_third: key # komment
list-only:
  - first # comment 2
  - third # I have a comment too
  - second # what?
simple-map:
  what-are-you-waiting-for: christmas? # duke nukem rulez
  jingle: bels # not christmas yet
map-of-maps:
  key:
    another-sub-key: w00t # casimir
    sub-key: sub-value # comment 3
    my-sub-key-name-is-longuer-than-yours: 1 # sentinel vs superman

"""

data = yaml.load(inp)


def my_add_eol_comment(self, comment, key=NotNone, column=None) -> None:  # noqa: ANN001
    """Provide a custom eol comment function."""
    org_col = column
    if column is None:
        try:
            column = self._yaml_get_column(key)
        except AttributeError:
            column = 0
    if comment[0] != "#":
        comment = "# " + comment
    if org_col != 0 and comment[0] == "#":  # only do this if the specified colunn is not the beginning of the line
        if org_col is None:
            comment = " " + comment
            column = 0
        else:
            comment = " " * (org_col - 1) + comment
            column = 0
    start_mark = CommentMark(column)
    ct = [CommentToken(comment, start_mark, None), None]
    self._yaml_add_eol_comment(ct, key=key)


CommentedBase.yaml_add_eol_comment = my_add_eol_comment  # pyright: ignore [ reportAttributeAccessIssue]


def process_comments(data: CommentedMap, column: int | None = None) -> None:  # noqa: C901
    """Process comments."""
    if isinstance(data, dict):
        if data.ca and data.ca.items:
            pprint(
                "CommentedMap with ca with items : " + str(data.ca.items),
                file=sys.stderr,
            )
            for key in data.ca.items:
                if data.ca.items[key][2]:
                    comment = data.ca.items[key][2].value.replace("\n", "")
                    try:
                        col = data._yaml_get_column(key)  # noqa: SLF001
                        pprint(
                            "key [" + key + "] at col [" + str(col) + "]",
                            file=sys.stderr,
                        )
                    except AttributeError:
                        pprint(
                            "key [" + key + "] at col [EXCEPTION]",
                            file=sys.stderr,
                        )
                    data.yaml_add_eol_comment(comment, key, column=column)
        for k, v in data.items():
            process_comments(k, column=column)
            process_comments(v, column=column)
    elif isinstance(data, list):
        if data.ca and data.ca.items:
            pprint(
                "CommentedSeq with ca with items : " + str(data.ca.items),
                file=sys.stderr,
            )
            for key in data.ca.items:
                if data.ca.items[key][0]:
                    comment = data.ca.items[key][0].value.replace("\n", "")
                    data.yaml_add_eol_comment(comment, key, column=column)
        for elem in data:
            process_comments(elem, column=column)


process_comments(data, column=2)
yaml.dump(data, sys.stdout)
