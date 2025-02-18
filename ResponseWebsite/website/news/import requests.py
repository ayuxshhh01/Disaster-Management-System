import requests
from django.http import JsonResponse

def prediction_view(request):
    try:
        # Fetch weather data
        weather_url = "http://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=5c6621d889d5bb4d009983274a99c9fe"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()  # Raise error if request fails
        weather_data = weather_response.json()

        # Fetch earthquake data
        earthquake_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson"
        earthquake_response = requests.get(earthquake_url, timeout=10)
        earthquake_response.raise_for_status()
        earthquake_data = earthquake_response.json()

        # Debugging: Print data in the console
        print("Weather Data:", weather_data)
        print("Earthquake Data:", earthquake_data)

        context = {
            'weather': weather_data,
            'earthquakes': earthquake_data.get("features", [])
        }
        return JsonResponse(context)  # Return JSON instead of rendering a template

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
