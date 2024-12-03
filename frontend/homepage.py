import streamlit as st
import requests

# Set page config
st.set_page_config(layout="wide", page_title="Vibers")

# Base URL for the Flask backend
BASE_URL = "http://127.0.0.1:5000"

# Navigation bar
selected = st.selectbox("Main Menu", ["Flights", "My Trips", "Web Scraping", "Login", "Sign Up"])

if selected == "Flights":
    st.title("Vibers")
    st.header("Search Flights")

    # Flight search form
    trip_type = st.radio("Trip Type:", ["Round Trip", "One Way"])
    col1, col2 = st.columns(2)
    from_city = col1.text_input("Where from?")
    to_city = col2.text_input("Where to?")
    departure_date = st.date_input("Departure")
    return_date = st.date_input("Return") if trip_type == "Round Trip" else None

    if st.button("Search for Flights"):
        # Prepare data for the backend
        params = {
            'origin': from_city,
            'destination': to_city,
            'departure_date': departure_date.isoformat()
        }
        response = requests.get(f"{BASE_URL}/api/scrape-flights", params=params)

        if response.status_code == 200:
            flight_data = response.json()
            if flight_data:
                st.table(flight_data)

                # Display "Book Flight" button for each flight data entry
                for index, flight in enumerate(flight_data):
                    flight_info = f"Flight: {flight['flight_name']}, Date: {flight['flight_date']}, Price: {flight['fare']}"
                    if st.button(f"Book {flight_info}", key=f"book_{index}"):  # Use 'key' to make each button unique
                        booking_data = {
                            "trip_id": flight.get("trip_id", "TBD"),  # Replace with actual data if available
                            "ticket_id": flight.get("ticket_id", "TBD"),  # Replace with actual data if available
                            "flight_name": flight["flight_name"],
                            "flight_date": flight["flight_date"],
                            "fare": flight["fare"]
                        }
                        booking_response = requests.post(f"{BASE_URL}/api/book-flight", json=booking_data)

                        if booking_response.status_code == 201:
                            st.success(f"Flight {flight['flight_name']} booked successfully!")
                        else:
                            st.error(f"Failed to book flight {flight['flight_name']}. Please try again later.")
            else:
                st.info("No flight data available.")
        else:
            st.error("Failed to fetch flight data. Please try again later.")

elif selected == "My Trips":
    st.title("Flight History")
    response = requests.get(f"{BASE_URL}/api/flight-history")
    if response.status_code == 200:
        flight_history = response.json()
        if flight_history:
            st.table(flight_history)
        else:
            st.info("No flight history available.")
    else:
        st.error(response.json().get("error", "Failed to fetch flight history."))

elif selected == "Web Scraping":
    st.title("Web Scraping")
    st.header("Scraped Flight Data")
    st.info("Use the 'Search for Flights' section to initiate flight data scraping.")

elif selected == "Login":
    st.title("Login")
    st.header("Sign In to Your Account")

    with st.form(key="login_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        sign_in = st.form_submit_button("SIGN IN")

        if sign_in:
            response = requests.post(f"{BASE_URL}/api/login", json={
                "email": email,
                "password": password
            })
            if response.status_code == 200:
                st.success("Logged in successfully!")
            else:
                st.error(response.json().get("error", "Incorrect email or password"))

elif selected == "Sign Up":
    st.title("Sign Up")
    st.header("Create a New Account")

    with st.form(key="signup_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        agree_terms = st.checkbox("I agree to the Terms of Service")
        register = st.form_submit_button("REGISTER")

        if register:
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif not agree_terms:
                st.error("Please agree to the Terms of Service.")
            else:
                response = requests.post(f"{BASE_URL}/api/register", json={
                    "name": name,
                    "email": email,
                    "password": password
                })
                if response.status_code == 201:
                    st.success("Registration successful!")
                else:
                    st.error(response.json().get("error", "Registration failed."))
