# Editor integration

This guide shows how to run `yamkix` from your editor.

## VSCode Task

- Install the package with `uv tool install yamkix` (or `pip install --user yamkix` if you are not using [uv](https://docs.astral.sh/uv/concepts/tools/))

- Sample **vscode** task :

<!-- end list -->

``` json
{
  "label": "format yaml with yamkix",
  "type": "shell",
  "command": "yamkix --input ${file}",
  "group": "build",
  "presentation": {
    "reveal": "always",
    "panel": "shared"
  },
  "problemMatcher": []
}
```
