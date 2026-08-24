from user_notes.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_produces_different_hash_than_plain():
    hashed = hash_password("password123")

    assert hashed != "password123"


def test_verify_password_succeeds_with_correct_password():
    hashed = hash_password("password123")

    assert verify_password("password123", hashed) is True


def test_verify_password_fails_with_wrong_password():
    hashed = hash_password("password123")

    assert verify_password("wrongpassword", hashed) is False


def test_create_and_decode_access_token_roundtrip():
    token = create_access_token({"sub": "42"})

    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "42"
    assert "exp" in payload


def test_decode_invalid_token_returns_none():
    assert decode_access_token("not-a-valid-token") is None


def test_decode_tampered_token_returns_none():
    token = create_access_token({"sub": "42"})

    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")

    assert decode_access_token(tampered) is None
