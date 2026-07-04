# Install instructions

## Install `Yamkix`

- `Yamkix` is published on [pypi.org](https://pypi.org/project/yamkix/)
- You can make it available in your path with [uv](https://docs.astral.sh/uv/guides/tools/) (for instance):

```shell
uv tool install yamkix
```

## Installing `Yamkix` with `mise`

- [mise](https://mise.jdx.dev/) is an awesome tool that can install softwares in different versions (compared to `brew`)
- `mise` provides a [pipx backend](https://mise.jdx.dev/dev-tools/backends/pipx.html) ... that can rely on `uv` if available

```toml title="Sample mise.toml"
[tools]
"pipx:pre-commit" = { version = "4.3.0", uvx_args = "--with pre-commit-uv" }
"pipx:yamkix" = "0.10.0"
shellcheck = "0.11.0"
shfmt = "3.12.0"
uv = "0.8.9"
```
