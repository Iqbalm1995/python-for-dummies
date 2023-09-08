from database import db

class User(db.Model):
    __tablename__ = 'usr_users'  # Set your custom table name here


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    created_by = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)
    updated_by = db.Column(db.String(255), nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)