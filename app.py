from flask import Flask, url_for, request, redirect, make_response, abort, render_template
import datetime
from datetime import timedelta
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)


if app.config['DB_TYPE'] == 'postgres':
    db_name = 'dar_redkacheva_orm'
    db_user = 'dar_redkacheva_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "dar_redkacheva_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)


log404 = []
@app.errorhandler(404)
def not_found(err):
    time = datetime.datetime.today()
    client_ip = request.remote_addr
    url = request.url

    log404.append((time, client_ip, url))
    log_html = "<ul>"
    for time, client_ip, url in log404:
        log_html += "<li>" + str(time) + " — " + str(client_ip) + " — " + str(url) + "</li>"
    log_html += "</ul>"

    return '''
<!doctype html>
<html>
    <head>
        <title>Страница не найдена</title>
        <style>
            body {
                background-color: #f0f0f0;
                text-align: center;
                font-family: Arial, sans-serif;
                color: #333;
                padding: 20px;
            }
            h1 {
                font-size: 60px;
                color: #e74c3c;
            }
            p {
                font-size: 20px;
                color: #e74c3c;
            }
            img {
                margin-top: 30px;
                width: 400px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #fff;
                background-color: black;
                padding: 10px 20px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Упс! Похоже, такой страницы не существует.</p>
        <img src="https://www.meme-arsenal.com/memes/ad5d93d7683adb4c781adc5f82dbc437.jpg" alt="404 Not Found">
        <br>
        <p><b>Ваш IP:</b> ''' + str(client_ip) + '''</p>
        <p><b>Дата доступа:</b> ''' + str(time) + '''</p>
        <p><b>Запрошенный адрес:</b> ''' + str(url) + '''</p>
        <a href="/">Вернуться на главную</a>
        <h2>Журнал обращений с ошибкой 404</h2>
        ''' + log_html + '''
    </body>
</html>
''', 404


@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>
            body {
                background-color: #FFD1D5;;
                margin: 0;
            }
            nav {
                font-size: 15px;
                font-family 'Times New Roman', Times, serif;
                color: white;
            }
            header {
                background-color: rgb(219, 112, 147);
                color: white;
                padding: 10px;
                font-family: Georgia, 'Times New Roman', Times, serif;
                text-align: center;
                font-size: 10px;
            }
            footer {
                background-color: rgb(219, 112, 147);
                color: white;
                padding: 10px;
                font-family: Georgia, 'Times New Roman', Times, serif;
                font-style: italic;
                text-align: right;
                position: fixed;
                bottom: 0;
                right: 0;
                left: 0;
                z-index: 2;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <nav>
            <ul>
                <li><a href="/lab1">Лабораторная работа 1</a></li>
            </ul>
            <ul>
                <li><a href="/lab2">Лабораторная работа 2</a></li>
            </ul>
            <ul>
                <li><a href="/lab3/">Лабораторная работа 3</a></li>
            </ul>
            <ul>
                <li><a href="/lab4/">Лабораторная работа 4</a></li>
            </ul>
            <ul>
                <li><a href="/lab5">Лабораторная работа 5</a></li>
            </ul>
            <ul>
                <li><a href="/lab6/">Лабораторная работа 6</a></li>
            </ul>
            <ul>
                <li><a href="/lab7/">Лабораторная работа 7</a></li>
            </ul>
            <ul>
                <li><a href="/lab8/">Лабораторная работа 8</a></li>
            </ul>
            <ul>
                <li><a href="/lab9/">Лабораторная работа 9</a></li>
            </ul>
        </nav>
        <footer>
            Редкачева Дарина Вадимовна, группа ФБИ-32, 3 курс, 2025 год
        </footer>
    </body>
</html>
''' 


@app.errorhandler(500)
def internal_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
        <style>
            body {
                background-color: #f8d7da;
                color: #721c24;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            h1 {
                font-size: 60px;
            }
            p {
                font-size: 20px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #fff;
                background-color: #721c24;
                padding: 10px 20px;
                border-radius: 5px;
            }
            a:hover {
                background-color: #501217;
            }
        </style>
    </head>
    <body>
        <h1>500</h1>
        <p>Произошла внутренняя ошибка сервера.</p>
        <p>Попробуйте вернуться на главную страницу.</p>
        <a href="/">Главная</a>
    </body>
</html>
''', 500 