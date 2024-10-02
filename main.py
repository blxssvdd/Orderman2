from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orderman_v2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


API_KEY = '7e9ec6ca0de3d0263fe889837c0e7a87'
CITY_ID = 698740
CITY_NAME = 'Одеська область'


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)


def get_weather_by_id(city_id):
    url = f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return weather, temperature
    return None, None


@app.route('/')
def index():
    dishes = Dish.query.all()


    weather, temperature = get_weather_by_id(CITY_ID)


    if weather:
        if 'rain' in weather:
            recommendation = "До дощу чудово підійде піца з грибами!"
        elif 'clear' in weather:
            recommendation = "Сонячний день? Якраз час для піци Маргарита!"
        else:
            recommendation = "Чудовий вибір — піца Пепероні!"
    else:
        recommendation = "Не вдалося отримати інформацію про погоду."

    return render_template('index.html', dishes=dishes, weather=weather, temperature=temperature, recommendation=recommendation, city_name=CITY_NAME)


@app.route('/add_dish', methods=['POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        new_dish = Dish(name=name, description=description, price=price)
        db.session.add(new_dish)
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
