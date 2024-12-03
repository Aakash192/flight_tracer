from app import app, db

if __name__ == "__main__":
    # Ensure database tables are created
    with app.app_context():
        db.create_all()
    app.run(debug=True)
