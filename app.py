from flask import Flask, url_for, request, redirect, make_response, abort, render_template
import datetime
app = Flask(__name__)

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

@app.route("/lab1/web")
def web():
    return """<!doctype html>
         <html> 
            <body> 
                <h1>web-сервер на flask</h1> 
                <a href="/lab1/author">author</a>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

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

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <a href="/">На главную</a>
        <hr>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/reset_counter">/reset_counter</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/created">/lab1/created</a></li>
            <li><a href="/error400">/error400</a></li>
            <li><a href="/error401">/error401</a></li>
            <li><a href="/error402">/error402</a></li>
            <li><a href="/error403">/error403</a></li>
            <li><a href="/error405">/error405</a></li>
            <li><a href="/error418">/error418</a></li>
            <li><a href="/cause_error">/cause_error</a></li>
        </ul>
    </body>
</html>
'''

@app.route("/lab1/author")
def author():
    name = "Редкачева Дарина Вадимовна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html>" 
         <html> 
            <body> 
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="ждун.jpg")
    css_path = url_for("static", filename="lab1.css")

    html =  '''
    <!doctype html>
        <html> 
            <body> 
                <h1>Ждун</h1> 
                <img src="''' + path + '''">
                <link rel="stylesheet" href="''' + css_path + '''">
            </body>
        </html>
    '''
    headers = {
        "Content-Language": "ru",       
        "X-Author": "Redkacheva Darina", 
        "X-Lab": "Web-programming Lab1" 
    }
    return html, 200, headers

count = 0
@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
     <html> 
        <body> 
            Сколько раз вы сюда заходили: ''' + str(count) + '''
            <hr>
            Дата и время: ''' + str(time) + '''<br>
            Запрошенный адрес: ''' + str(url) + '''<br>
            Ваш IP-адрес: ''' + str(client_ip) + '''<br>
            <a href="/reset_counter">Сбросить счётчик</a>
        </body>
    </html>
'''
@app.route("/reset_counter")
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
    <html>
        <body>
            Счётчик был сброшен.<br>
            <a href="/lab1/counter">Вернуться к счётчику</a>
        </body>
    </html>
'''
@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def craeted():
    return '''
<!doctype html>
     <html> 
        <body> 
            <h1>Создано успешно</h1> 
            <div><i>что-то создано</i></div>
        </body>
    </html>
'''
@app.route("/error400")
def error400():
    return make_response("400 Bad Request — Некорректный запрос", 400)

@app.route("/error401")
def error401():
    return make_response("401 Unauthorized — Не авторизован", 401)

@app.route("/error402")
def error402():
    return make_response("402 Payment Required — Требуется оплата", 402)

@app.route("/error403")
def error403():
    return make_response("403 Forbidden — Доступ запрещён", 403)

@app.route("/error405")
def error405():
    return make_response("405 Method Not Allowed — Метод не разрешён", 405)

@app.route("/error418")
def error418():
    return make_response("418 I'm a teapot — Я — чайник", 418)


@app.route("/cause_error")
def cause_error():
    result = 1 / 0
    return "Результат: ''' + str(result) + ''' "

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

flower_list = ['мак', 'василек', 'гвоздика', 'георгин', 'пион']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else: 
        return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Выбранный цветок</h1>
            <p>Цветок: <b>{flower_list[flower_id]}</b></p>
            <p><a href="/lab2/all_flowers">Посмотреть все цветы</a></p>
        </body>
    </html>
    '''
@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>Список цветов очищен</h1>
            <p>Все цветы удалены из списка.</p>
            <p><a href="/lab2/all_flowers">Посмотреть список цветов</a></p>
        </body>
    </html>
    '''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html>
'''
@app.route('/lab2/add_flower/')
def add_flower_no_name():
    return "Вы не задали имя цветка", 400

@app.route('/lab2/all_flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Список всех цветов</h1>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''
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