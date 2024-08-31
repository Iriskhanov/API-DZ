import requests
from django.shortcuts import render
from . forms import CityForm


def to_prepositional(city_name):
    exceptions = {
        'Грозный': 'Грозном',
        'Москва': 'Москве',
        'Сочи': 'Сочи',
        'Тверь': 'Твери',
        'Нижний Новгород': 'Нижнем Новгороде',

    }

    if city_name in exceptions:
        return exceptions[city_name]    
    if city_name.endswith('ый'):
        return city_name[:-2] + 'ом'
    elif city_name.endswith('ий'):
        return city_name[:-2] + 'ем'
    elif city_name.endswith('ая'):
        return city_name[:-2] + 'ой'
    elif city_name.endswith('е'):
        return city_name
    elif city_name.endswith('а'):
        return city_name[:-1] + 'е'
    elif city_name.endswith('я'):
        return city_name[:-1] + 'е'
    else:
        return city_name + 'е'
    
def weather_forecast(city_name, temperature):
    city_name_prepositional = to_prepositional(city_name)
    return f"Погода в {city_name_prepositional}: {temperature} градусов."

def fetch_weather_data(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}&lang=ru'
    try:
        response = requests.get(url)
        response.raise_for_status
        return response.json()
    except requests.exceptions.RequestException:
        return None

def index(request):
    api_key = 'fe97831a39b3550a8d659fde90f2ca3e'
    form = CityForm(request.POST or None)
    weather = None

    if request.method == 'POST' and form.is_valid():
        city = form.cleaned_data['city']
        response = fetch_weather_data(city, api_key)

        if response and response.get('cod') == 200:
            weather = {
                    'city': city,
                    'temperature': response['main']['temp'],
                    'description': response['weather'][0]['description'].capitalize(),
                    'icon': response['weather'][0]['icon']
                }
        else:
            weather = None

    return render(request, 'index.html', {'form': form, 'weather': weather})



