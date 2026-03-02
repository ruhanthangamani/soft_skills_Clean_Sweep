import os
from flask import Flask, send_from_directory
from config.config import Config
from models.db import init_db
from routes.auth import auth_bp
from routes.events import events_bp

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
app.config.from_object(Config)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(events_bp, url_prefix='/api/events')

@app.route('/api/init-db')
def setup_db():
    from models.db import init_db
    try:
        init_db()
        return "Database initialized successfully! You can now log in.", 200
    except Exception as e:
        return f"Failed to initialize database: {e}", 500

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
