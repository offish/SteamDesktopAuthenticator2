import time

from flask import Flask, Response, abort, jsonify, redirect, render_template, request

from sda2.account_manager import AccountManager
from sda2.guard import generate_confirmation_key, generate_one_time_code

BASE_PATH = "/sda2/"
app = Flask(__name__)
account_manager = AccountManager()


@app.route("/")
def index() -> Response:
    return redirect("/decrypt")


@app.route(BASE_PATH)
def home() -> Response:
    return render_template("index.html", check_user_script_installed=True)


@app.route("/decrypt", methods=["GET", "POST"])
def descrypt() -> Response:
    if request.method == "POST":
        password = request.form.get("password", "").strip()

        try:
            account_manager.decrypt_accounts(password)
            print("Accounts decrypted successfully")
        except ValueError:
            pass

    if account_manager.needs_password():
        print("Password is required to access the accounts")
        return render_template(
            "index.html", password_required=True, check_user_script_installed=False
        )

    account_manager.set_remaining_accounts()
    return redirect(BASE_PATH)


@app.route(BASE_PATH + "codes")
def codes() -> Response:
    return render_template("codes.html", accounts=account_manager.get_accounts())


@app.route(BASE_PATH + "code/<username>")
def get_code(username: str) -> str:
    print(f"User requesting login code for {username}")
    shared_secret = account_manager.get_shared_secret(username)

    if not shared_secret:
        abort(404, description="No shared_secret was found for that username.")

    return generate_one_time_code(shared_secret)


@app.route(BASE_PATH + "key/<username>/<tag>")
def get_confirmation_key(username: str, tag: str) -> Response:
    print(f"User requesting confirmation key for {username}, tag {tag}")
    timestamp = int(request.args.get("t", time.time()))
    identity_secret = account_manager.get_identity_secret(username)

    if not identity_secret:
        abort(404, description="No identity_secret was found for that username.")

    return jsonify(
        {
            "time": timestamp,
            "key": generate_confirmation_key(identity_secret, tag, timestamp),
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
