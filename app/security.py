import secrets


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def mask_secret(value: str | None) -> str:
    if not value:
        return "Not configured"
    if len(value) <= 8:
        return "Configured"
    return f"{value[:4]}...{value[-4:]}"

