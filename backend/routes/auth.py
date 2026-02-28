from flask import Blueprint, request, jsonify, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([name, email, password, role]):
        return jsonify({'error': 'Missing fields'}), 400
    
    if role not in ['organizer', 'volunteer']:
        return jsonify({'error': 'Invalid role'}), 400

    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
                     (name, email, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already registered'}), 409
    finally:
        conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    print(f"DEBUG: Login attempt for email: {email}")

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user:
        print(f"DEBUG: User found in DB. Checking password...")
        is_correct = check_password_hash(user['password'], password)
        print(f"DEBUG: Password correct: {is_correct}")
        if is_correct:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            print(f"DEBUG: Login successful for {email}")
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200
    
    print(f"DEBUG: Login failed for {email}")
    return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify(None), 200 # Not logged in
    
    return jsonify({
        'id': session['user_id'],
        'name': session['name'],
        'role': session['role']
    }), 200
