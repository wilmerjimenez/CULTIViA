import requests

def fetch_open_meteo_data(lat, lon, start, end):
    url = 'https://archive-api.open-meteo.com/v1/era5'
    params = {
        'latitude': lat, 'longitude': lon,
        'start_date': start, 'end_date': end,
        'hourly': 'temperature_2m,precipitation,relative_humidity_2m'
    }
    response = requests.get(url, params=params)
    return response.json()
