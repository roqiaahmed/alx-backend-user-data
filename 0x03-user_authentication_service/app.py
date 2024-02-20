#!/usr/bin/env python3
"""Flask app
"""

from flask import Flask, jsonify, request, abort
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
        AUTH.create_session(email)
        return jsonify({"email": f"{email}", "message": "logged in"})
    return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
