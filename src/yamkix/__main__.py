"""Allow yamkix to be executable through `python -m yamkix`."""

from yamkix.typer_cli import app

if __name__ == "__main__":  # pragma: no cover
    app()
