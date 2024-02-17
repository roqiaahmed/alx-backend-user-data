#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """log in function"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or email is None:
        return jsonify({"error": "email missing"}), 400

    if not password or password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    valid_pass = user[0].is_valid_password(password)
    if not valid_pass:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)
    SESSION_NAME = getenv("SESSION_NAME")
    res = jsonify(user[0].to_json())
    res.set_cookie(SESSION_NAME, session_id)
    return res


@app_views.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """log out function"""
    from api.v1.app import auth

    del_session = auth.destroy_session(request)
    if del_session == False:
        abort(404)
    return jsonify({}), 200
