from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)


class VaultEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    site = db.Column(db.String(120), nullable=False)
    site_username = db.Column(db.String(120), nullable=False)
    encrypted_password = db.Column(db.String(300), nullable=False)