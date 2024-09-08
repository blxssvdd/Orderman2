from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    user_name = "Ярослав"
    return render_template('index.html', user_name=user_name)

@app.route('/menu')
def menu():
    pizzas = [
        {"name": "Маргарита", "description": "Сир, томатний соус, базилік", "price": 8.99},
        {"name": "Пепероні", "description": "Сир, томатний соус, пепероні", "price": 9.99},
        {"name": "Гавайська", "description": "Сир, томатний соус, ананас, шинка", "price": 10.99},
        {"name": "Вегетаріанська", "description": "Сир, овочі, томатний соус", "price": 7.99},
    ]


    sort_order = request.args.get('sort', 'asc')

    if sort_order == 'asc':
        pizzas = sorted(pizzas, key=lambda x: x['price'])
    elif sort_order == 'desc':
        pizzas = sorted(pizzas, key=lambda x: x['price'], reverse=True)

    return render_template('menu.html', pizzas=pizzas, sort_order=sort_order)

if __name__ == '__main__':
    app.run(debug=True)
