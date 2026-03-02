import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_clean_sweep'
    SUPABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:Ruhan%40221006@db.qwhngsneiryznespypkn.supabase.co:5432/postgres'
