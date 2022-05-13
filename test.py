import requests
from flask import Flask
import constants

app = Flask(__name__)


@app.route('/')
def test():
    city = 'Las Vegas'

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'

    res = requests.get(url.format(city, constants.API_KEY)).json()

    weather = {
        'city': city,
        'temp': res['main']['temp'],
        'des': res['weather'][0]['description']
    }
    print(res)
    print(weather)
    return ''


if __name__ == '__main__':
    app.run(debug=True)
