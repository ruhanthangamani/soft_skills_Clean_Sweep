import os

# Set Vercel environment so config.py knows to use /tmp for SQLite
os.environ['VERCEL'] = '1'

import sys
# Add the backend directory to Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

from app import app

# Vercel requires the variable to be named `app`
