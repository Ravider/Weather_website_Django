import requests
from django.shortcuts import render

def weather_view(request):
    city = request.GET.get('city', 'Delhi')  # Default city
    weather_data = {}
    photo_url = None
    popular_place_url = None

    # OpenWeatherMap API
    weather_api_key = '1e45a1073c885c08634b8a1352ad8a24'
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    weather_response = requests.get(weather_url).json()

    if weather_response.get('cod') == 200:  # Successful response
        weather_data = {
            'city': city,
            'temperature': weather_response['main']['temp'],
            'icon': weather_response['weather'][0]['icon'],
            'description': weather_response['weather'][0]['description']
        }

    # Unsplash API for City Photo
    unsplash_api_key = 'YOUR_UNSPLASH_API_KEY'
    unsplash_url = f"https://api.unsplash.com/search/photos?query={city}&client_id={unsplash_api_key}&per_page=1"
    unsplash_response = requests.get(unsplash_url).json()

    if unsplash_response.get('results'):
        photo_url = unsplash_response['results'][0]['urls']['regular']

    # Google Places API for Popular Place Photo
    google_places_api_key = 'YOUR_GOOGLE_PLACES_API_KEY'
    places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=popular+places+in+{city}&key={google_places_api_key}"
    places_response = requests.get(places_url).json()

    if places_response.get('results'):
        place_photo_reference = places_response['results'][0].get('photos', [{}])[0].get('photo_reference')
        if place_photo_reference:
            popular_place_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={place_photo_reference}&key={google_places_api_key}"

    return render(request, 'weather/index.html', {
        'weather_data': weather_data,
        'photo_url': photo_url,
        'popular_place_url': popular_place_url
    })
