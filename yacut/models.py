from datetime import datetime

from yacut import db


class URLMap(db.Model):
    __tablename__ = 'db.sqlite3'

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False, unique=True)
    short = db.Column(db.String(50), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
