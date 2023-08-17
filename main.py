import os
from flask import Flask, render_template, request, flash, redirect, make_response

app = Flask(__name__)

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)
static = os.path.join(
    package_dir, "static"
)
app.static_folder=static
app.config['SECRET_KEY'] = 'qwerty!QAZ'

category = [
    {"name": "Одежда", "id": 1},
    {"name": "Обувь", "id": 2},
    {"name": "Аксессуары", "id": 3},
]


@app.route('/')
def index():
    user_data = request.cookies.get('user_data')
    if user_data:
        cookies = (dict(i.split('=', 1) for i in user_data.split('&')))
        return render_template('index.html', user=cookies)
    return render_template('index.html', user=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_data = request.cookies.get('user_data')
    if user_data:
        cookies = (dict(i.split('=', 1) for i in user_data.split('&')))
        return render_template('login.html', user=cookies)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        if username and email:
            flash("Successful login", "success")
            response = make_response(redirect('/'))
            response.set_cookie('user_data', f'username={username}&email={email}')
            return response
        else:
            flash("Wrong username or email", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('user_data')
    return response


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
