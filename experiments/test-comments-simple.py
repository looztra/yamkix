"""Test comments on a very simple CommentedMap."""
import sys
import ruamel.yaml


comment_column = None
insert = ruamel.yaml.comments.CommentedMap()
insert["test"] = "asdf"
insert.yaml_add_eol_comment("Test Comment!", "test", column=comment_column)
insert["second-key"] = "yop"
insert.yaml_add_eol_comment(
    "Another comment", "second-key", column=comment_column
)

yaml = ruamel.yaml.YAML()
yaml.dump(insert, sys.stdout)
