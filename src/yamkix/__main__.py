"""Allow yamkix to be executable through `python -m yamkix`."""

from yamkix._cli import app  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    app()
