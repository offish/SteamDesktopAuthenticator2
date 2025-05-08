import json
from pathlib import Path
from typing import Any

MAFILES_PATH = Path(__file__).parent.parent / "maFiles"


def get_account_file_path(username: str, has_file_extension: bool = False) -> Path:
    file_name = username

    if not has_file_extension:
        file_name += ".maFile"

    return MAFILES_PATH / file_name


def load_secret(username: str) -> dict:
    secret_path = get_account_file_path(username)

    if not secret_path.exists():
        raise FileNotFoundError(f"No account data was found for username: {username}")

    data = {}

    # TODO: handle encryption
    with open(secret_path, "r") as f:
        data = json.loads(f.read())

    return data


def get_manifest() -> dict | None:
    manifest_path = MAFILES_PATH / "manifest.json"

    if not manifest_path.exists():
        return

    with open(manifest_path, "r") as f:
        manifest = json.loads(f.read())

    return manifest


def get_accounts() -> list[str]:
    accounts = []

    for file in MAFILES_PATH.glob("*.maFile"):
        accounts.append(file.stem)

    return accounts


def get_secret_value(username: str, key: str) -> Any:
    return load_secret(username).get(key, None)


def get_identity_secret(username: str) -> str:
    return get_secret_value(username, "identity_secret")


def get_shared_secret(username: str) -> str:
    return get_secret_value(username, "shared_secret")
