from app import load_token


def test_token_is_truthy() -> None:
    # Weak: only checks that a value exists.
    assert load_token()
