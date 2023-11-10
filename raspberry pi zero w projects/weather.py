import requests
from datetime import datetime

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "7fbc35b1f6d5fa5074a88fd88c8e32c3"
CITY = "Meppen"

def get_weather(api_key, location):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric")
    data = response.json()

    # Durchschnittstemperatur berechnen
    temp_sum = 0
    for i in range(8):
        temp_sum += data['list'][i]['main']['temp']
    avg_temp = temp_sum / 8
    print(f"Durchschnittstemperatur für den Tag: {avg_temp}°C")

    # Stündliche Temperatur anzeigen
    for i in range(8):
        time = datetime.utcfromtimestamp(data['list'][i]['dt']).hour
        temp = data['list'][i]['main']['temp']
        print(f"{time} Uhr: {temp}°C")

# Ersetzen Sie 'your_api_key' durch Ihren tatsächlichen API-Schlüssel und 'your_location' durch Ihren Standort
get_weather(API_KEY, CITY)
