from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(),
                                                     Length(min=3, max=30,
                                                            message="Пароль должен содержать не менее 3 и не более 30 "
                                                                    "символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    firstname = StringField("Имя: ", validators=[DataRequired(), Length(min=2, max=100,
                                                                        message="Имя должно быть от "
                                                                                "2до 100 символов")])
    lastname = StringField("Фамилия: ", validators=[DataRequired(), Length(min=3, max=100,
                                                                           message="Фамилия должно быть от "
                                                                                   "2 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100,
                                                       message="Пароль должен быть от 4 до 100 символов")])
    # submit = SubmitField("Регистрация")
