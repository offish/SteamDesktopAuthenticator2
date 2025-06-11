import json
from pathlib import Path

from .decryption import decrypt_data


class AccountManager:
    def __init__(self) -> None:
        self.mafiles_path = Path(__file__).parent.parent / "maFiles"
        self._accounts = {}
        self._password = None

    @property
    def manifest_path(self) -> Path:
        return self.mafiles_path / "manifest.json"

    def needs_password(self) -> bool:
        return self._password is None and self.accounts_are_encrypted()

    def has_manifest(self) -> bool:
        return self.manifest_path.exists()

    def accounts_are_encrypted(self) -> bool:
        if not self.has_manifest():
            return False

        manifest = self.read_manifest()
        return manifest.get("encrypted", False)

    def set_account(self, username: str, data: dict) -> None:
        self._accounts[username] = data

    def get_accounts(self) -> list[str]:
        return list(self._accounts.keys())

    def set_remaining_accounts(self) -> None:
        for file in self.mafiles_path.glob("*.maFile"):
            try:
                data = {}

                with open(file, "r") as f:
                    data = json.load(f)

                username = data["account_name"]

                if username not in self._accounts:
                    self.set_account(username, data)

            except json.JSONDecodeError:
                pass

    def read_manifest(self) -> dict:
        content = {}

        with open(self.manifest_path, "r") as f:
            content = json.load(f)

        return content

    def get_secret_value(self, username: str, key: str) -> str | None:
        if username not in self._accounts:
            raise ValueError(f"No account data found for username: {username}")

        return self._accounts[username].get(key, None)

    def get_identity_secret(self, username: str) -> str:
        return self.get_secret_value(username, "identity_secret")

    def get_shared_secret(self, username: str) -> str:
        return self.get_secret_value(username, "shared_secret")

    def decrypt_accounts(self, password: str) -> None:
        self._password = password
        manifest = self.read_manifest()
        entries = manifest["entries"]

        for entry in entries:
            file_name = entry["filename"]
            salt = entry["encryption_salt"]
            iv = entry["encryption_iv"]
            path = self.mafiles_path / file_name

            if not path.exists():
                print(f"No account data was found for file: {file_name}")
                continue

            try:
                encrypted_data = open(path, "rb").read()
                decrypted = decrypt_data(password, salt, iv, encrypted_data)
                data = json.loads(decrypted)
                username = data["account_name"]
                self.set_account(username, data)

            except UnicodeDecodeError:
                print(f"Failed to decode data for {file_name}")
