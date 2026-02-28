from flask import Blueprint, request, jsonify, session
from models.db import get_db_connection
import sqlite3

events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['GET'])
def get_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY date ASC').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in events])

@events_bp.route('/', methods=['POST'])
def create_event():
    if 'user_id' not in session or session.get('role') != 'organizer':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    date = data.get('date')
    category = data.get('category')
    image_url = data.get('image_url')

    if not all([title, description, location, date, category]):
        return jsonify({'error': 'Missing fields'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO events (organizer_id, title, description, location, date, category, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (session['user_id'], title, description, location, date, category, image_url))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Event created successfully'}), 201

@events_bp.route('/<int:event_id>/join', methods=['POST'])
def join_event(event_id):
    if 'user_id' not in session or session.get('role') != 'volunteer':
        return jsonify({'error': 'Unauthorized'}), 403

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO signups (event_id, volunteer_id) VALUES (?, ?)',
                     (event_id, session['user_id']))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Already joined this event'}), 409
    finally:
        conn.close()

    return jsonify({'message': 'Joined event successfully'}), 200

@events_bp.route('/my-events', methods=['GET'])
def my_events():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    if session['role'] == 'organizer':
        events = conn.execute('SELECT * FROM events WHERE organizer_id = ?', (session['user_id'],)).fetchall()
    else:
        # For volunteers, fetch events they signed up for
        events = conn.execute('''
            SELECT e.* FROM events e
            JOIN signups s ON e.id = s.event_id
            WHERE s.volunteer_id = ?
        ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return jsonify([dict(ix) for ix in events])

@events_bp.route('/<int:event_id>/participants', methods=['GET'])
def get_event_participants(event_id):
    if 'user_id' not in session or session.get('role') != 'organizer':
        return jsonify({'error': 'Unauthorized'}), 403

    conn = get_db_connection()
    # verify event belongs to organizer
    event = conn.execute('SELECT organizer_id FROM events WHERE id = ?', (event_id,)).fetchone()
    if not event:
        conn.close()
        return jsonify({'error': 'Event not found'}), 404
        
    # Ideally should check if event['organizer_id'] == session['user_id']
    # But for now, any organizer can view (as per initial plan simplification, but lets be safe)
    if event['organizer_id'] != session['user_id']:
         conn.close()
         return jsonify({'error': 'Unauthorized to view these participants'}), 403

    participants = conn.execute('''
        SELECT u.name, u.email, s.signup_date
        FROM users u
        JOIN signups s ON u.id = s.volunteer_id
        WHERE s.event_id = ?
    ''', (event_id,)).fetchall()
    
    conn.close()
    return jsonify([dict(ix) for ix in participants])

@events_bp.route('/<int:event_id>/status', methods=['POST'])
def update_event_status(event_id):
    if 'user_id' not in session or session.get('role') != 'organizer':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    status = data.get('status')
    if not status:
        return jsonify({'error': 'Missing status'}), 400

    conn = get_db_connection()
    # verify event belongs to organizer
    event = conn.execute('SELECT organizer_id FROM events WHERE id = ?', (event_id,)).fetchone()
    if not event:
        conn.close()
        return jsonify({'error': 'Event not found'}), 404
        
    if event['organizer_id'] != session['user_id']:
         conn.close()
         return jsonify({'error': 'Unauthorized to modify this event'}), 403

    conn.execute('UPDATE events SET status = ? WHERE id = ?', (status, event_id))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Event status updated to {status}'}), 200
