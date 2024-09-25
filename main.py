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

    def __repr__(self):
        return f'<Dish {self.name}>'


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Position {self.title}>'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    position = db.relationship('Position', backref=db.backref('employees', lazy=True))

    def __repr__(self):
        return f'<Employee {self.name} - {self.position.title}>'


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu():
    all_dishes = Dish.query.all()
    return render_template('menu.html', dishes=all_dishes)


@app.route('/admin/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])

        new_dish = Dish(name=name, description=description, price=price)
        db.session.add(new_dish)
        db.session.commit()

        return redirect(url_for('menu'))

    return render_template('add_dish.html')


@app.route('/employees')
def employees():
    all_employees = Employee.query.all()
    return render_template('employees.html', employees=all_employees)


@app.route('/admin/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position_title = request.form['position']


        position = Position.query.filter_by(title=position_title).first()
        if not position:
            position = Position(title=position_title)
            db.session.add(position)


        new_employee = Employee(name=name, position=position)
        db.session.add(new_employee)
        db.session.commit()

        return redirect(url_for('employees'))

    return render_template('add_employee.html')

if __name__ == '__main__':
    app.run(debug=True)
