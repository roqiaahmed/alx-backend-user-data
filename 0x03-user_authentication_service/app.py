#!/usr/bin/env python3
"""Flask app
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    user_email = request.form.get("email")
    user_password = request.form.get("password")
    try:
        AUTH.register_user(user_email, user_password)
        return jsonify({"email": f"{user_email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """login method"""
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout method"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("index"))
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    "profile method"
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    user_email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(user_email)
        return jsonify({"email": user_email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """update password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")
