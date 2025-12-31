# auth.py
from flask import request, abort, jsonify, session
from werkzeug.security import check_password_hash
from models import User

def login():
    """
    Standard Login: Checks credentials and sets a Session Cookie.
    """
    # 1. Get JSON data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 2. Find User
    user = User.query.filter_by(email=email).one_or_none()

    # 3. Check Password (Secure Hash check)
    # Note: Ensure you store passwords using generate_password_hash() in your seed script!
    if user and user.password and check_password_hash(user.password, password):
        # --- SUCCESS: SAVE TO SESSION ---
        session['user_id'] = user.user_id
        session['role'] = user.role.role_name.lower()
        return jsonify({"message": "Logged in successfully"}), 200
    
    abort(401, "Invalid Credentials")

def logout():
    """
    Clears the session.
    """
    session.clear()
    return jsonify({"message": "Logged out"}), 200