import time

from flask import Flask, Response, abort, jsonify, redirect, render_template, request

from sda2.guard import generate_confirmation_key, generate_one_time_code
from sda2.utils import get_identity_secret, get_shared_secret

BASE_PATH = "/sda2/"
app = Flask(__name__)


@app.route("/")
def index() -> Response:
    return redirect("/sda2/")


@app.route(BASE_PATH)
def sda2() -> Response:
    return render_template("index.html")


@app.route(BASE_PATH + "/code/<username>")
def get_code(username: str) -> str:
    print(f"User requesting login code for {username}")

    shared_secret = get_shared_secret(username)

    if not shared_secret:
        abort(404, description="No shared_secret was found for that username.")

    return generate_one_time_code(shared_secret)


@app.route(BASE_PATH + "/key/<username>/<tag>")
def get_confirmation_key(username: str, tag: str) -> Response:
    print(f"User requesting confirmation key for {username}, tag {tag}")

    timestamp = int(request.args.get("t", time.time()))
    identity_secret = get_identity_secret(username)

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
