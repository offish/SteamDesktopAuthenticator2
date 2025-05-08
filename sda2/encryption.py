import base64
import json
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .utils import get_account_file_path, get_manifest

PBKDF2_ITERATIONS = 50000
SALT_LENGTH = 8
KEY_SIZE_BYTES = 32
IV_LENGTH = 16

backend = default_backend()


def get_random_salt() -> bytes:
    return base64.b64encode(os.urandom(SALT_LENGTH)).decode("utf-8")


def get_initialization_vector() -> bytes:
    return base64.b64encode(os.urandom(IV_LENGTH)).decode("utf-8")


def get_encryption_key(password: str, salt_b64: str) -> bytes:
    salt = base64.b64decode(salt_b64)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=KEY_SIZE_BYTES,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=backend,
    )
    return kdf.derive(password.encode())


def encrypt_data(password: str, salt_b64: str, iv_b64: str, plaintext: str) -> str:
    key = get_encryption_key(password, salt_b64)
    iv = base64.b64decode(iv_b64)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    # PKCS7 Padding
    pad_len = 16 - (len(plaintext.encode()) % 16)
    padded = plaintext.encode() + bytes([pad_len] * pad_len)

    ct = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(ct).decode()


def decrypt_data(
    password: str, salt_b64: str, iv_b64: str, encrypted_data_b64: str | bytes
) -> str:
    key = get_encryption_key(password, salt_b64)
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(encrypted_data_b64)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    pad_len = padded_plaintext[-1]
    return padded_plaintext[:-pad_len].decode()


def decrypt_account(password: str, steam_id: int) -> dict:
    accounts = get_manifest()["entries"]

    for account in accounts:
        if account["steamid"] == steam_id:
            path = get_account_file_path(account["filename"], True)
            break

    if not path or not path.exists():
        raise FileNotFoundError(
            f"No account data was found for that SteamID {steam_id}"
        )

    try:
        data = open(path, "rb").read()
        decrypted = decrypt_data(
            password,
            account["encryption_salt"],
            account["encryption_iv"],
            data,
        )

        return json.loads(decrypted)
    except UnicodeDecodeError:
        return None
