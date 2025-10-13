from flask import Blueprint, url_for, request, redirect, make_response, abort
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
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


@lab1.route("/lab1")
def lab():
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


@lab1.route("/lab1/author")
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


@lab1.route("/lab1/image")
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
@lab1.route("/lab1/counter")
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


@lab1.route("/reset_counter")
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
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


@lab1.route("/error400")
def error400():
    return make_response("400 Bad Request — Некорректный запрос", 400)


@lab1.route("/error401")
def error401():
    return make_response("401 Unauthorized — Не авторизован", 401)


@lab1.route("/error402")
def error402():
    return make_response("402 Payment Required — Требуется оплата", 402)


@lab1.route("/error403")
def error403():
    return make_response("403 Forbidden — Доступ запрещён", 403)


@lab1.route("/error405")
def error405():
    return make_response("405 Method Not Allowed — Метод не разрешён", 405)


@lab1.route("/error418")
def error418():
    return make_response("418 I'm a teapot — Я — чайник", 418)


@lab1.route("/cause_error")
def cause_error():
    result = 1 / 0
    return "Результат: ''' + str(result) + ''' "

