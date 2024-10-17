from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orderman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)



@app.route('/')
def index():
    dishes = Dish.query.all()
    return render_template('index.html', dishes=dishes)


@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])

        new_dish = Dish(name=name, description=description, price=price)
        db.session.add(new_dish)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_dish.html')


@app.route('/edit_dish/<int:id>', methods=['GET', 'POST'])
def edit_dish(id):
    dish = Dish.query.get_or_404(id)
    if request.method == 'POST':
        dish.name = request.form['name']
        dish.description = request.form['description']
        dish.price = float(request.form['price'])

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_dish.html', dish=dish)


@app.route('/delete_dish/<int:id>')
def delete_dish(id):
    dish = Dish.query.get_or_404(id)
    db.session.delete(dish)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
