import requests
from bs4 import BeautifulSoup

def scrape_flight_data(origin, destination, departure_date):
    # Replace with the actual URL of the site you want to scrape
    url = f"https://www.ca.kayak.com/flights?lang=en&skipapp=true&gclid=CjwKCAiA0rW6BhAcEiwAQH28Ip9bdvodgFc5XSSm7DVUTObwTgbQjiLmcwDNZNapQhu4ZSIdHOzwxxoCnSkQAvD_BwE&aid=99663193861"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from the website.")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract flight data (update the selectors based on actual site structure)
    flights = []
    for flight in soup.find_all('div', class_='flight-details'):  # Replace with actual tag and class
        flight_data = {
            'flight_number': flight.find('span', class_='flight-number').text,
            'departure_time': flight.find('span', class_='departure-time').text,
            'arrival_time': flight.find('span', class_='arrival-time').text,
            'price': flight.find('span', class_='price').text,
        }
        flights.append(flight_data)
    
    return flights
