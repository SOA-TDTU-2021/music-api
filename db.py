from config import sql
from datetime import datetime, timedelta
import math, random, uuid

class User(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100))
    email = sql.Column(sql.String(120), unique=True)
    password_hash = sql.Column(sql.String(100))
    roles = sql.Column(sql.Integer)
    avatar_file = sql.Column(sql.String(100))
    date_created = sql.Column(sql.DateTime, default=datetime.now)
    otp_code = sql.Column(sql.String(10))
    otp_expiration_datetime = sql.Column(sql.DateTime, default=datetime(1970, 1, 1))
