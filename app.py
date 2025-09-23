from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404
@app.route("/")
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

from flask import Flask

app = Flask(__name__)

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