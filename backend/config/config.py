import os
import shutil

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_clean_sweep'
    
    if os.environ.get('VERCEL'):
        orig_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'clean_sweep.db')
        tmp_db_path = '/tmp/clean_sweep.db'
        
        # On Vercel cold starts, copy the committed DB (with users/events) to the writable /tmp directory
        if not os.path.exists(tmp_db_path) and os.path.exists(orig_db_path):
            try:
                shutil.copy2(orig_db_path, tmp_db_path)
            except Exception as e:
                print(f"Error copying DB to /tmp: {e}")
                
        DB_PATH = tmp_db_path
    else:
        DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'clean_sweep.db')
