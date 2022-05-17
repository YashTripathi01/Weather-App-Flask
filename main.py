import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#import constants

# initializing the flask app
app = Flask(__name__)
# config value for the database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# to use flash we need secret key
app.config['SECRET_KEY'] = constants.SECRET_KEY

# initialize the sqlalchemy class
db = SQLAlchemy(app)

# create a sqlalchemy class which inherits from db.Model


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)


# function that gets the data for the cities if exists
def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={constants.API_KEY}'
    response = requests.get(url).json()

    return response


# creating routes


@app.route('/')
def root_get():
    # to loop over the cities and get the info
    cities = City.query.all()

    # to hold the data after looping of every city
    weather_data = []

    # city = 'Tokyo'

    # for each city in the db it is going to send the request to the api, getting the weather for that city
    for city in cities:
        # storing the requests from the api
        response = get_weather_data(city.city_name)

        # dictionary to hold filtered data
        weather = {
            'city': city.city_name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }

        # appending the list
        weather_data.append(weather)

    # print(response)
    # print(weather_data)

    return render_template('home.html', weather_data=weather_data)


@app.route('/', methods=['POST'])
def root_post():
    error_msg = ''
    new_city = request.form.get('city')

    if new_city:
        existing_city = City.query.filter_by(city_name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = City(city_name=new_city)

                db.session.add(new_city_obj)
                db.session.commit()
                db.session.close()
            else:
                error_msg = 'What kind of city is this, Dummy!'
        else:
            error_msg = 'City already exists in the database!'

    if error_msg:
        flash(error_msg, 'error')
    else:
        flash('City added successfully!')

    return redirect(url_for('root_get'))


# delete route
@app.route('/delete<city_name>')
def delete_city(city_name):
    city = City.query.filter_by(city_name=city_name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted {city.city_name}', 'success')
    return redirect(url_for('root_get'))


if __name__ == '__main__':
    app.run(debug=True)


'''
{'coord': {'lon': -115.1372, 'lat': 36.175}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 16.24, 'feels_like': 14.42, 'temp_min': 14.54, 'temp_max': 17.37, 'pressure': 1018, 'humidity': 19}, 'visibility': 10000, 'wind': {'speed': 3.09, 'deg': 250}, 'clouds': {'all': 20}, 'dt': 1652328305, 'sys': {'type': 2, 'id': 2016943, 'country': 'US', 'sunrise': 1652272661, 'sunset': 1652322974}, 'timezone': -25200, 'id': 5506956, 'name': 'Las Vegas', 'cod': 200}
'''
