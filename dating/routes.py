from flask import Blueprint, render_template, request, redirect, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from dating.models import DatingUser

dating = Blueprint('dating', __name__, template_folder='templates')


# --- Главная страница ---
@dating.route('/')
def index():
    return render_template('dating/index.html')


# --- Регистрация ---
@dating.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('dating/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    full_name = request.form.get('full_name')
    group_name = request.form.get('group_name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    search_gender = request.form.get('search_gender')

    if DatingUser.query.filter_by(login=login_form).first():
        flash("Такой логин уже существует", "error")
        return redirect('/dating/register')

    user = DatingUser(
        login=login_form,
        password_hash=generate_password_hash(password_form),
        full_name=full_name,
        group_name=group_name,
        age=int(age),
        gender=gender,
        search_gender=search_gender
    )
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect('/dating/')


# --- Вход ---
@dating.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('dating/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    user = DatingUser.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password_hash, password_form):
        login_user(user)
        return redirect('/dating/')
    
    flash("Логин или пароль неверны", "error")
    return redirect('/dating/login')


# --- Выход ---
@dating.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/dating/')


# --- Профиль пользователя ---
@dating.route('/me', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('dating/profile.html', user=current_user)

    # Обновление анкеты
    current_user.full_name = request.form.get('full_name')
    current_user.group_name = request.form.get('group_name')
    current_user.age = int(request.form.get('age'))
    current_user.gender = request.form.get('gender')
    current_user.search_gender = request.form.get('search_gender')
    current_user.about = request.form.get('about')
    current_user.is_hidden = bool(request.form.get('is_hidden'))
    
    db.session.commit()
    flash("Анкета обновлена", "success")
    return redirect('/dating/me')


# --- Поиск пользователей с постраничным выводом ---
@dating.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    page = request.args.get('page', 1, type=int)
    per_page = 3
    results = []

    name_query = ''
    age_query = ''

    if request.method == 'POST':
        # Сохраняем фильтры в сессии, чтобы можно было листать страницы
        name_query = request.form.get('name', '').strip()
        age_query = request.form.get('age', '').strip()
        session['search_name'] = name_query
        session['search_age'] = age_query
    else:
        # GET-запрос, берем фильтры из сессии
        name_query = session.get('search_name', '')
        age_query = session.get('search_age', '')

    query = DatingUser.query.filter(
        DatingUser.id != current_user.id,
        DatingUser.is_hidden == False,
        DatingUser.gender == current_user.search_gender,
        DatingUser.search_gender == current_user.gender
    )

    if name_query:
        query = query.filter(DatingUser.full_name.ilike(f"%{name_query}%"))
    if age_query.isdigit():
        query = query.filter(DatingUser.age == int(age_query))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    results = pagination.items

    return render_template('dating/search.html', results=results, pagination=pagination)
