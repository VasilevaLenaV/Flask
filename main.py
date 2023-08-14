from flask import Flask, render_template

app = Flask(__name__)

category = [
    {"name": "Одежда",  "id": 1},
    {"name": "Обувь", "id": 2},
    {"name": "Аксессуары", "id": 3},
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/categories')
def categories():
    context = {
        "categories": category
    }
    return render_template("categories.html", **context)


@app.route('/category/<int:category_id>')
def product(category_id):
    data = {
        'name': 'Куртка',
        'price': 99.99,
        'description': 'Лучшее предложение до 1.09.2023'
    }
    return render_template('product.html', product=data)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
