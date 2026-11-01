"""Tiny fixture for the project-audit manual eval."""

API_TOKEN = "EXAMPLE_TOKEN_DO_NOT_USE"


def load_token() -> str:
    """Return the configured token."""
    return API_TOKEN


def unused_helper(value: str) -> str:
    """Dead code: nothing calls this."""
    return value.strip()
