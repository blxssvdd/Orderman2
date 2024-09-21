import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)

DATABASE = 'menu.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS dishes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      description TEXT NOT NULL,
                      price REAL NOT NULL)''')
        db.commit()


@app.route('/')
def index():
    user_name = "Ярослав"
    return render_template('index.html', user_name=user_name)


@app.route('/menu')
def menu():
    sort_order = request.args.get('sort', 'asc')
    query = 'SELECT name, description, price FROM dishes'

    if sort_order == 'asc':
        query += ' ORDER BY price ASC'
    else:
        query += ' ORDER BY price DESC'

    dishes = query_db(query)

    total_price = sum([dish[2] for dish in dishes])

    return render_template('menu.html', dishes=dishes, sort_order=sort_order, total_price=total_price)


@app.route('/admin/add', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        db = get_db()
        db.execute('INSERT INTO dishes (name, description, price) VALUES (?, ?, ?)',
                   (name, description, float(price)))
        db.commit()

        return redirect(url_for('menu'))

    return render_template('add_dish.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
