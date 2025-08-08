import requests
import sys
from config import api_key

def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 1)

def wind_direction(deg):
    dirs = ['հյուսիսային', 'հս-արևելյան', 'արևելյան', 'հս-արևմտյան',
            'հարավային', 'հս-արևմտյան', 'արևմտյան', 'հս-արևմտյան']
    ix = round(deg / 45) % 8
    return dirs[ix]

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code != 200:
            print(f"❌ Սխալ քաղաք կամ բանալի ({data.get('message', 'Սխալ հարցում')})")
            return

        name = data['name']
        weather = data['weather'][0]['description'].capitalize()
        temp = kelvin_to_celsius(data['main']['temp'])
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        wind_dir = wind_direction(wind_deg)

        print(f"\n📍 {name} 🌤")
        print(f"Ջերմաստիճան՝ {temp}°C")
        print(f"Եղանակ՝ {weather}")
        print(f"Քամի՝ {wind_dir}, {wind_speed} մ/վ")
        print(f"Խոնավություն՝ {humidity}%\n")

    except requests.exceptions.RequestException:
        print("❌ Չհաջողվեց կապ հաստատել։ Ստուգիր ինտերնետդ։")

def main():
    if len(sys.argv) < 2:
        print("Օգտագործում՝ python weather.py <քաղաք>")
        return

    city = " ".join(sys.argv[1:])
    get_weather(city)

if __name__ == "__main__":
    main()
