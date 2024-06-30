from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    address_line1 = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(20))
    user_type = db.Column(db.String(20))
