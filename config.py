from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+USER+":"+PASS+"@"+SERVER+"/"+DB_NAME
sql = SQLAlchemy(app)
