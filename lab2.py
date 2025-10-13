from flask import Blueprint, url_for, request, redirect, make_response, abort, render_template
import datetime
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/')
def labb():
    return render_template('lab2.html')


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [ 
    {'name': 'мак', 'price': 50},
    {'name': 'василек', 'price': 60},
    {'name': 'гвоздика', 'price': 70},
    {'name': 'георгин', 'price': 80},
    {'name': 'пион', 'price': 120},
]

@lab2.route('/lab2/flowers/<int:flower_id>')
def flower_detail(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower_detail.html', flower=flower, flower_id=flower_id)



@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('all_flowers'))


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('all_flowers'))


@lab2.route('/lab2/add_flower', methods=['POST'])
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
    flower_list.lab2end({'name': name, 'price': price_val})
    return redirect(url_for('all_flowers'))


@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', flower_list=flower_list)


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</> чудных..."
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
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


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
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

@lab2.route("/lab2/books_list")
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

@lab2.route("/lab2/memes")
def memes_pict():
    return render_template("memes.html", memes=memes)