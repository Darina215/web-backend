from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/lab1/web")
def web():
    return """<!doctype html>
         <html> 
            <body> 
                <h1>web-сервер на flask</h1> 
                <a href="/author">author</a>
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
    </body>
</html>
'''

@app.route("/lab1/author")
def author():
    name = "Редкачева Дарина Вадимовна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html>" 
         </html> 
            </body> 
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="ждун.jpg")
    css_path = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
     <html> 
        <body> 
            <h1Ждун</h1> 
            <img src="''' + path + '''">
            <link rel="stylesheet" href="''' + css_path + '''">
        </body>
    </html>
'''
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
            <a href="/counter">Вернуться к счётчику</a>
        </body>
    </html>
'''
@app.route("/lab1/info")
def info():
    return redirect("/author")


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
    return make_response("418 I'm a teapot — Я — чайник (шутка RFC 2324)", 418)
