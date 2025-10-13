from flask import Flask, url_for, request, redirect, make_response, abort, render_template
import datetime
from lab1 import lab1
app = Flask(__name__)
app.register_blueprint(lab1)

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
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
            <ul>
                <li><a href="/lab2">Вторая лабораторная</a></li>
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

#---------------------------------------------------------Лабораторная 2 ---------------------------------------------------------
@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [ 
    {'name': 'мак', 'price': 50},
    {'name': 'василек', 'price': 60},
    {'name': 'гвоздика', 'price': 70},
    {'name': 'георгин', 'price': 80},
    {'name': 'пион', 'price': 120},
]

@app.route('/lab2/flowers/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower_detail.html', flower=flower, flower_id=flower_id)

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('all_flowers'))

@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('all_flowers'))

@app.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '').strip()
    if not name:
        return redirect(url_for('all_flowers'))
    try:
        price_val = int(price)
    except Exception:
        try:
            price_val = float(price)
        except Exception:
            price_val = 0
    flower_list.append({'name': name, 'price': price_val})
    return redirect(url_for('all_flowers'))

@app.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', flower_list=flower_list)

@app.route('/lab2/example')
def example():
    name = 'Редкачева Дарина'
    count_lab = 2
    group = 'ФБИ-32'
    course = 3
    fruits = [
        {'name': 'бананы', 'price': 100},
        {'name': 'апельсины', 'price': 120},
        {'name': 'киви', 'price': 80},
        {'name': 'арбузы', 'price': 95},
        {'name': 'персики', 'price': 200}
    ]
    return render_template('example.html', 
        name=name,
        count_lab=count_lab,
        group=group,
        course=course,
        fruits=fruits
    )

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a,b):
    add_res = a + b 
    sub_res = a - b 
    mul_res = a * b 
    div_res = None if b == 0 else a / b 
    pow_res = a ** b 

    div_text = 'делить на 0 нельзя &#9940;' if div_res is None else f'{div_res}'
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Расчет с параметрами:</h1>
        <div>
            {a} + {b} = {add_res} <br>
            {a} - {b} = {sub_res} <br>
            {a} × {b} = {mul_res} <br>
            {a} / {b} = {div_text} <br>
            {a}<sup>{b}</sup> = {pow_res} <br>
        </div>
    </body>
</html>
'''
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_one_param(a):
    return redirect(url_for('calc', a=a, b=1))

books = [
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Анна Каренина", "title": "Лев Толстой", "genre": "Роман", "pages": 864},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Поэма", "pages": 224},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Роман", "pages": 432},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 384},
    {"author": "Антон Чехов", "title": "Вишнёвый сад", "genre": "Пьеса", "pages": 128},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Роман", "pages": 448},
    {"author": "Сергей Есенин", "title": "Стихотворения", "genre": "Поэзия", "pages": 192},
    {"author": "Борис Пастернак", "title": "Доктор Живаго", "genre": "Роман", "pages": 592},
]

@app.route("/lab2/books_list")
def books_list():
    return render_template("books.html", books=books)

memes = [
    {"name": "Мем №1", "image": "#mems.jfif", "description": "Приятный плакат."},
    {"name": "Мем №2", "image": "бокал.jfif", "description": "Пес в бокале."},
    {"name": "Мем №3", "image": "веселый.jfif", "description": "Веселый)"},
    {"name": "Мем №4", "image": "грустный.jfif", "description": "Грустный("},
    {"name": "Мем №5", "image": "довольный.jfif", "description": "Хихик."},
    {"name": "Мем №6", "image": "загрузки.jfif", "description": "Не понял."},
    {"name": "Мем №7", "image": "заяц.jfif", "description": "Когда получил автомат по web-программированию"},
    {"name": "Мем №8", "image": "Клоун.jfif", "description": "Я."},
    {"name": "Мем №9", "image": "кокетка.jfif", "description": "Кокетка."},
    {"name": "Мем №10", "image": "кот_шок.jfif", "description": "Увидел цены на что-либо."},
    {"name": "Мем №11", "image": "кот_думает.jfif", "description": "Загадочный."},
    {"name": "Мем №12", "image": "ненехочу.jfif", "description": "Поступай в магистратуру!"},
    {"name": "Мем №13", "image": "сердечко.jfif", "description": "Всем кто это увидел )))"},
    {"name": "Мем №14", "image": "собака_релакс.jfif", "description": "Скоро день рождения.."},
    {"name": "Мем №15", "image": "стая.jfif", "description": "Да."},
    {"name": "Мем №16", "image": "трудовые.jfif", "description": "Базовый минимум."},
    {"name": "Мем №17", "image": "фиолетовый.jfif", "description": "Вливаюсь в новую компанию."},
    {"name": "Мем №18", "image": "язык.jfif", "description": "Хихик)"},
    {"name": "Мем №19", "image": "язык2.jpg", "description": "Прикольный."},
    {"name": "Мем №20", "image": "кот.jfif", "description": "Конец!"}
]

@app.route("/lab2/memes")
def memes_pict():
    return render_template("memes.html", memes=memes)