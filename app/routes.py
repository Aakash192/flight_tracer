from flask import Flask, request, jsonify
from app import app, db
from app.models import User, FlightHistory
from werkzeug.security import generate_password_hash, check_password_hash
from app.scraper import scrape_flight_data
import traceback

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flight Management API!"})

# User registration route
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Fetch flight history route
@app.route('/api/flight-history', methods=['GET'])
def flight_history():
    try:
        flights = FlightHistory.query.all()
        results = [
            {
                "trip_id": flight.trip_id,
                "ticket_id": flight.ticket_id,
                "flight_name": flight.flight_name,
                "flight_date": flight.flight_date,
                "fare": flight.fare
            }
            for flight in flights
        ]
        return jsonify(results), 200
    except Exception as e:
        app.logger.error(f"Error in /api/flight-history: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Add flight route (for testing or manual entry)
@app.route('/api/add-flight', methods=['POST'])
def add_flight():
    try:
        data = request.get_json()
        required_fields = ["trip_type", "from_city", "to_city", "departure_date"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        new_flight = FlightHistory(
            trip_id=1,  # Replace with unique trip ID logic
            ticket_id="TBD",  # Replace with ticket ID logic
            flight_name=f"{data['from_city']} to {data['to_city']}",
            flight_date=data['departure_date'],
            fare="TBD"  # Replace with fare logic
        )
        db.session.add(new_flight)
        db.session.commit()
        return jsonify({"message": "Flight added successfully!"}), 201
    except Exception as e:
        app.logger.error(f"Error in /api/add-flight: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Scrape flights route
@app.route('/api/scrape-flights', methods=['GET'])
def scrape_flights():
    try:
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        departure_date = request.args.get('departure_date')

        flight_data = scrape_flight_data(origin, destination, departure_date)
        return jsonify(flight_data), 200
    except Exception as e:
        app.logger.error(f"Error in /api/scrape-flights: {e}")
        return jsonify({"error": str(e)}),
