def optional_int(value: str | int | None) -> int | None:
    if value in (None, ""):
        return None
    return int(value)

