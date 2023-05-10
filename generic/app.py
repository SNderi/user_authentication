#!/usr/bin/env python3
"""Flask application."""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def hello():
    """Function to display Welcome message."""
    return jsonify({"message": "Welcome"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Function to add user to db"""
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """End-point to login users."""
    email = request.form['email']
    password = request.form['password']

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        sess_id = AUTH.create_session(email)
        res = make_response(jsonify({"email": email, "message": "logged in"}))
        res.set_cookie("session_id", sess_id)
        return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """End-point to logout users. """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """End-point to get users profiles. """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """End-point to handle password resets."""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
