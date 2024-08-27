import requests
from django.shortcuts import render
from . forms import CityForm


def index(request):
    api_key = 'fe97831a39b3550a8d659fde90f2ca3e'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key + '&lang=ru'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            response = requests.get(url.format(city)).json()

            if response['cod'] == 200:
                weather = {
                    'city': city,
                    'temperature': response['main']['temp'],
                    'description': response['weather'][0]['description'].capitalize(),
                    'icon': response['weather'][0]['icon']
                }
            else:
                weather = None
        else:
            weather = None
    else:
        form = CityForm()
        weather = None

    return render(request, 'index.html', {'form': form, 'weather': weather})


