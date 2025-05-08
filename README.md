# SteamDesktopAuthenticator2
[![Stars](https://img.shields.io/github/stars/offish/SteamDesktopAuthenticator2.svg)](https://github.com/offish/SteamDesktopAuthenticator2/stargazers)
[![Issues](https://img.shields.io/github/issues/offish/SteamDesktopAuthenticator2.svg)](https://github.com/offish/SteamDesktopAuthenticator2/issues)
[![Size](https://img.shields.io/github/repo-size/offish/SteamDesktopAuthenticator2.svg)](https://github.com/offish/SteamDesktopAuthenticator2)
[![Discord](https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord)](https://discord.gg/t8nHSvA)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

SteamDesktopAuthenticator2 (SDA2) allows you to confirm trade and market transactions directly from your browser. While it is named SDA2 for convenience, it is not affiliated with [Jessecar96](https://github.com/Jessecar96) or the original [SteamDesktopAuthenticator](https://github.com/Jessecar96/SteamDesktopAuthenticator) project. SDA2 was created because the original SDA project is no longer receiving updates and has become slow when there are many pending confirmations.

## Showcase
![Untitled](https://github.com/user-attachments/assets/55b27733-55b3-4639-92d5-70cf564cf0ef)

## Features
- Mass Accept Transactions: Quickly accept multiple trade offers and transactions.
- Uses Current Account: It automatically uses the account you are logged into.
- Automatic Redirect: Automatically redirects you when a confirmation is needed for sending a Trade Offer.

## What do I need?
- Unencrypted maFile(s) for the account(s) you want to use with SDA2
- Python 3 installed
- A browser with the Tampermonkey extension

> [!CAUTION]
> NEVER share your `maFiles`, `password`, `shared_secret` or `identity_secret` with ANYONE. If these are present in logs or similar, remove them before submitting an issue.

## Donate
- BTC: `bc1q9gmh5x2g9s0pw3282a5ypr6ms8qvuxh3fd7afh`
- [Steam Trade Offer](https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR)

## Setup
Clone the repository.
Place your maFile(s) inside the `maFiles` directory. These has to be unencrypted.

> [!IMPORTANT]
> The maFile(s) has to be unencrypted.

The name of each file must on the format: `accountName.maFile` where accountName is the Steam account name (not alias) e.g. `gaben123.maFile`.

```bash
pip install -r requirements.txt
python main.py
```

Open your browser which has Tampermonkey installed.

### [Install the Tampermonkey user script](https://github.com/offish/SteamDesktopAuthenticator2/raw/refs/heads/main/userscript/SteamDesktopAuthenticator2.user.js)

Now you can go to http://127.0.0.1:5000/sda2/ to confirm trade and market transactions.
You need to allow Tampermonkey to make requests.

> [!NOTE]
> You can also use https://doctormckay.github.io/steam-twofactor-server/ to confirm your trades. Set the 2FA Server Base URL to `http://127.0.0.1:5000/sda2/`

## Acknowledgements
- [Alex Corn](https://github.com/DoctorMcKay) ([steam-twofactor-server](https://github.com/DoctorMcKay/steam-twofactor-server)) - This repository is basically just a fork of `steam-twofactor-server` with the server ported to Python and minor changes to McKay's user script.
- [Michał Bukowski](https://github.com/bukson) ([steampy](https://github.com/bukson/steampy)) - Steam Guard functionality was taken from the implementation in `steampy`.
- [Samuel Breznjak](https://github.com/ekmas) ([cs16.css](https://github.com/ekmas/cs16.css)) - Styling used for the UI.
