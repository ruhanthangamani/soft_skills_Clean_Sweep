import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_clean_sweep'
    SUPABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres.qwhngsneiryznespypkn:Ruhan%40221006@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres?sslmode=require'
