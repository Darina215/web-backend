from flask import Blueprint, render_template, request, make_response, redirect
from datetime import datetime
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'Аноним')
    age = request.cookies.get('age', 'неизвестен')
    name_color = request.cookies.get('name_color', 'black')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    #кофе 120 рублей, черный чай 80, зеленый 70.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    #молоко +30 рублей, сахар +10
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    shadow = request.args.get('shadow') 

    if color or bgcolor or fontsize or shadow is not None:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bgcolor:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize:
            resp.set_cookie('fontsize', fontsize)
        if shadow is not None:
            resp.set_cookie('shadow', 'true')
        else:
            resp.set_cookie('shadow', '', expires=0)  
        return resp

    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    shadow = request.cookies.get('shadow') == 'true'

    return render_template('lab3/settings.html', color=color, bgcolor=bgcolor, fontsize=fontsize, shadow=shadow)


@lab3.route('/lab3/del_settings')
def del_settings():
    resp = make_response(redirect('/lab3/settings'))

    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bgcolor', '', expires=0)
    resp.set_cookie('fontsize', '', expires=0)
    resp.set_cookie('shadow', '', expires=0)

    return resp


SHEETS = ['нижняя', 'верхняя', 'верхняя боковая', 'нижняя боковая']

@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket_form():
    errors = {}
    values = {}

    if request.method == 'POST':
        
        values['full_name'] = request.form.get('full_name', '').strip()
        values['sheet'] = request.form.get('sheet', '')
        values['with_linens'] = request.form.get('with_linens') == 'on'
        values['with_baggage'] = request.form.get('with_baggage') == 'on'
        values['age'] = request.form.get('age', '').strip()
        values['from_point'] = request.form.get('from_point', '').strip()
        values['to_point'] = request.form.get('to_point', '').strip()
        values['travel_date'] = request.form.get('travel_date', '').strip()
        values['insurance'] = request.form.get('insurance') == 'on'

        if not values['full_name']:
            errors['full_name'] = 'ФИО обязательно.'
        if values['sheet'] not in SHEETS:
            errors['sheet'] = 'Выберите полку.'
        if not values['age']:
            errors['age'] = 'Возраст обязателен.'
        else:
            try:
                age_int = int(values['age'])
                if age_int < 1 or age_int > 120:
                    errors['age'] = 'Возраст должен быть от 1 до 120.'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом.'
        if not values['from_point']:
            errors['from_point'] = 'Пункт выезда обязателен.'
        if not values['to_point']:
            errors['to_point'] = 'Пункт назначения обязателен.'
        if not values['travel_date']:
            errors['travel_date'] = 'Дата поездки обязательна.'

        if not errors:
            age_int = int(values['age'])
            price = 1000 if age_int >= 18 else 700
            if values['sheet'] in ['нижняя', 'нижняя боковая']:
                price += 100
            if values['with_linens']:
                price += 75
            if values['with_baggage']:
                price += 250
            if values['insurance']:
                price += 150

            ticket = {
                'full_name': values['full_name'],
                'sheet': values['sheet'],
                'with_linens': values['with_linens'],
                'with_baggage': values['with_baggage'],
                'age': age_int,
                'from_point': values['from_point'],
                'to_point': values['to_point'],
                'travel_date': values['travel_date'],
                'insurance': values['insurance'],
                'price': price,
                'is_child': age_int < 18
            }
            return render_template('lab3/ticket.html', ticket=ticket)

    return render_template('lab3/ticket_form.html', sheets=SHEETS, values=values, errors=errors)


PRODUCTS = [
    {"name": "Мягкая игрушка медведь", "price": 500, "brand": "TeddyCo", "age": "3+"},
    {"name": "Конструктор LEGO Classic", "price": 1200, "brand": "LEGO", "age": "5+"},
    {"name": "Пазл 1000 элементов", "price": 650, "brand": "PuzzleWorld", "age": "8+"},
    {"name": "Кукла Барби", "price": 800, "brand": "Mattel", "age": "3+"},
    {"name": "Машинка Hot Wheels", "price": 300, "brand": "Mattel", "age": "4+"},
    {"name": "Набор Play-Doh", "price": 450, "brand": "Hasbro", "age": "3+"},
    {"name": "Робот-трансформер", "price": 1500, "brand": "Robotics", "age": "6+"},
    {"name": "Детский велосипед", "price": 4000, "brand": "Velokids", "age": "5+"},
    {"name": "Кубики деревянные", "price": 350, "brand": "WoodToys", "age": "2+"},
    {"name": "Игровой набор кухня", "price": 1800, "brand": "KidKraft", "age": "3+"},
    {"name": "Мягкая игрушка слон", "price": 550, "brand": "TeddyCo", "age": "3+"},
    {"name": "Железная дорога", "price": 2200, "brand": "Thomas", "age": "4+"},
    {"name": "Набор для рисования", "price": 700, "brand": "Crayola", "age": "4+"},
    {"name": "Кукла LOL", "price": 950, "brand": "MGA", "age": "5+"},
    {"name": "Машинка на радиоуправлении", "price": 1800, "brand": "RCWorld", "age": "6+"},
    {"name": "Игровой набор ферма", "price": 1300, "brand": "PlayBig", "age": "3+"},
    {"name": "Плюшевый зайчик", "price": 400, "brand": "TeddyCo", "age": "3+"},
    {"name": "Конструктор металлический", "price": 1600, "brand": "MechToys", "age": "7+"},
    {"name": "Набор для лепки", "price": 600, "brand": "Hasbro", "age": "3+"},
    {"name": "Детский самокат", "price": 3500, "brand": "ScooterKids", "age": "4+"},
]

@lab3.route('/lab3/products', methods=['GET', 'POST'])
def products():
    prices = [p['price'] for p in PRODUCTS]
    overall_min = min(prices)
    overall_max = max(prices)

    cookie_min = request.cookies.get('min_price')
    cookie_max = request.cookies.get('max_price')

    # Начальные значения для формы
    min_price = request.form.get('min_price', cookie_min)
    max_price = request.form.get('max_price', cookie_max)

    filtered = PRODUCTS

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'reset':
            resp = make_response(render_template('lab3/products.html',
                                                 products=PRODUCTS,
                                                 count=len(PRODUCTS),
                                                 min_price='',
                                                 max_price='',
                                                 overall_min=overall_min,
                                                 overall_max=overall_max))
            resp.set_cookie('min_price', '', expires=0)
            resp.set_cookie('max_price', '', expires=0)
            return resp

        if action == 'search':
            try:
                min_val = float(request.form.get('min_price')) if request.form.get('min_price') else None
            except ValueError:
                min_val = None
            try:
                max_val = float(request.form.get('max_price')) if request.form.get('max_price') else None
            except ValueError:
                max_val = None

            # Автоматически исправляем, если min > max
            if min_val is not None and max_val is not None and min_val > max_val:
                min_val, max_val = max_val, min_val

            def check_price(p):
                if min_val is not None and p['price'] < min_val:
                    return False
                if max_val is not None and p['price'] > max_val:
                    return False
                return True

            filtered = [p for p in PRODUCTS if check_price(p)]

            # Сохраняем выбранные значения в cookies
            resp = make_response(render_template('lab3/products.html',
                                                 products=filtered,
                                                 count=len(filtered),
                                                 min_price=min_val if min_val is not None else '',
                                                 max_price=max_val if max_val is not None else '',
                                                 overall_min=overall_min,
                                                 overall_max=overall_max))
            if min_val is not None:
                resp.set_cookie('min_price', str(min_val))
            if max_val is not None:
                resp.set_cookie('max_price', str(max_val))
            return resp

    # Если пользователь ранее заходил — показываем фильтрованные товары по cookies
    if cookie_min or cookie_max:
        try:
            min_val = float(cookie_min) if cookie_min else None
        except ValueError:
            min_val = None
        try:
            max_val = float(cookie_max) if cookie_max else None
        except ValueError:
            max_val = None

        if min_val is not None and max_val is not None and min_val > max_val:
            min_val, max_val = max_val, min_val

        def check_price(p):
            if min_val is not None and p['price'] < min_val:
                return False
            if max_val is not None and p['price'] > max_val:
                return False
            return True

        filtered = [p for p in PRODUCTS if check_price(p)]
        min_price = min_val if min_val is not None else ''
        max_price = max_val if max_val is not None else ''

    return render_template('lab3/products.html',
                           products=filtered,
                           count=len(filtered),
                           min_price=min_price,
                           max_price=max_price,
                           overall_min=overall_min,
                           overall_max=overall_max)