from app import db

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
# Flight history model
class FlightHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, nullable=False)
    ticket_id = db.Column(db.String(50), nullable=False)
    flight_name = db.Column(db.String(100), nullable=False)
    flight_date = db.Column(db.String(20), nullable=False)
    fare = db.Column(db.String(10), nullable=False)
