# HOSTNAME = "127.0.0.1"
# PORT = 3306
# DATABASE = "flaskdb"
# USERNAME = "root"
# PASSWORD = "20030418"
# DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URI = DB_URI
# SECRET_KEY = "123456"

import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
