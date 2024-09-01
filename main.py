from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    user_name = "Ярослав" # Ім'я я написав своє.
    return render_template('index.html', user_name=user_name)

@app.route('/menu')
def menu():
    pizzas = [
        {"name": "Маргарита", "description": "Сир, томатний соус, базилік", "price": "$8.99"},
        {"name": "Пепероні", "description": "Сир, томатний соус, пепероні", "price": "$9.99"},
        {"name": "Гавайська", "description": "Сир, томатний соус, ананас, шинка", "price": "$10.99"},
    ]
    return render_template('menu.html', pizzas=pizzas)

if __name__ == '__main__':
    app.run(debug=True)
