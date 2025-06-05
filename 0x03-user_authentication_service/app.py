#!/usr/bin/env python3
"""
Flask application for user authentication service.
Provides endpoints for user registration, login, logout,
profile access, and password reset functionality.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome message route.
    
    Returns:
        A JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register a new user.
    
    Returns:
        A JSON payload with the user email and success message,
        or an error message if the user already exists.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Log in a user and create a session.
    
    Returns:
        A JSON payload with the user email and success message,
        or aborts with 401 if login is invalid.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not AUTH.valid_login(email, password):
        abort(401)
    
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Log out a user by destroying the session.
    
    Returns:
        Redirects to home page if successful, or aborts with 403 if not.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    
    if user is None:
        abort(403)
    
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Get user profile.
    
    Returns:
        A JSON payload with the user email if session is valid,
        or aborts with 403 if not.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    
    if user is None:
        abort(403)
    
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_token() -> str:
    """Get a reset password token.
    
    Returns:
        A JSON payload with the user email and reset token,
        or aborts with 403 if email is not registered.
    """
    email = request.form.get('email')
    
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Update user's password.
    
    Returns:
        A JSON payload with the user email and success message,
        or aborts with 403 if reset token is invalid.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
