"""Provide the custom Yamkix errors."""


class InvalidTypValueError(ValueError):
    """Exception raised for invalid --typ option value."""

    def __init__(self, typ: str) -> None:
        """Create a new instance of InvalidTypValueError."""
        super().__init__(f"'{typ}' is not a valid value for option --typ. Allowed values are 'safe' and 'rt'")
