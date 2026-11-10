from pathlib import Path

from steampie import MaFileSummary as MaFile
from steampie import get_mafile_data, is_mafile_unencrypted

MAFILES_PATH = Path(__file__).parent.parent / "maFiles"
MAFILES = list(MAFILES_PATH.glob("*.maFile"))


class AccountManager:
    def __init__(self):
        self._accounts: dict[str, MaFile] = {}
        self._configured_accounts: set[Path] = set()
        self._accounts_set = False

    @property
    def accounts_set(self) -> bool:
        return self._accounts_set

    def needs_password(self) -> bool:
        return any(
            mafile not in self._configured_accounts
            and not is_mafile_unencrypted(mafile)
            for mafile in MAFILES
        )

    def ensure_setup(self) -> None:
        if not self._accounts_set and not self.needs_password():
            self.setup_accounts()

    def setup_accounts(self, code: str | None = None) -> None:
        for mafile in MAFILES:
            if mafile in self._configured_accounts:
                continue

            data = get_mafile_data(mafile, code)
            username = data["username"]

            self._accounts[username] = data
            self._configured_accounts.add(mafile)

        self._accounts_set = True

    def get_accounts(self) -> list[str]:
        return list(self._accounts.keys())

    def account_exists(self, username: str) -> None:
        if username not in self._accounts:
            raise ValueError(f"No account data found for username: {username}")

    def get_identity_secret(self, username: str) -> str | None:
        self.account_exists(username)
        return self._accounts[username]["identity_secret"]

    def get_shared_secret(self, username: str) -> str | None:
        self.account_exists(username)
        return self._accounts[username]["shared_secret"]
