import json
from pathlib import Path
from typing import Any

MAFILES_PATH = Path(__file__).parent.parent / "maFiles"


def load_secret(username) -> dict:
    secret_path = MAFILES_PATH / f"{username}.maFile"

    if not secret_path.exists():
        raise FileNotFoundError(
            f"No account data was found for that username: {username}"
        )

    data = {}

    # TODO: handle encryption
    with open(secret_path, "r") as f:
        data = json.loads(f.read())

    return data


def get_secret_value(username: str, key: str) -> Any:
    return load_secret(username).get(key, None)


def get_identity_secret(username: str) -> str:
    return get_secret_value(username, "identity_secret")


def get_shared_secret(username: str) -> str:
    return get_secret_value(username, "shared_secret")
