import os
import sqlite3

from forms import LoginForm, RegisterForm
from flask import Flask, render_template, request, flash, g, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from store import StoreDB
from user import User

app = Flask(__name__)

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)
static = os.path.join(
    package_dir, "static"
)

app.static_folder = static
app.config['SECRET_KEY'] = '271a5bbcf10532ae3ac2ae16e6c267cc5b3a5e9bef88d9e3'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "success"

category = [
    {"name": "Одежда", "id": 1},
    {"name": "Обувь", "id": 2},
    {"name": "Аксессуары", "id": 3},
]


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return User().from_db(user_id, dbase)


def connect_db():
    conn = sqlite3.connect('store.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = StoreDB(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    return render_template('index.html', user=None)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template('profile.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    email = form.login.data
    password = form.password.data

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.login.data)
        if user and check_password_hash(user['password'], form.password.data):
            user_ = User().create(user)
            rm = form.remember.data
            login_user(user_, remember=rm)
            return redirect(request.args.get("next") or url_for("index"))

        flash("Неверный логин или пароль", "error")

    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    firstname = form.firstname.data
    lastname = form.lastname.data
    email = form.email.data

    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        # (request.form['password'])

        res, err = dbase.add_user(firstname, lastname, hash, email)
        if res:
            flash("Вы зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash(f"Ошибка регистрации: {err}", "error")

    return render_template("register.html", title="Регистрация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/clear', methods=["GET", "POST"])
def clear():
    user_id = current_user.get_id()
    logout_user()
    if User().del_user(user_id, dbase):
        flash("Аккаунт успешно удален", "success")

    return redirect(url_for('login'))


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
