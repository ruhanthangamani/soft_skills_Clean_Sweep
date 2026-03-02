import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_clean_sweep'
    SUPABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres.qwhngsneiryznespypkn:Ruhan%40221006@aws-0-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require'
