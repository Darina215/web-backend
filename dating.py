from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

dating = Blueprint('dating', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
GENDERS = ['Мужской', 'Женский']

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='darina_dating',
            user='darina_dating',
            password='12345'
        )
        conn.set_client_encoding('UTF8')
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --------------------- Маршруты ---------------------

@dating.route('/')
def index():
    return render_template('dating/index.html', authorized='user_id' in session, login=session.get('login'))

@dating.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('dating/register.html')
    
    login = (request.form.get('login') or '').strip()
    password = (request.form.get('password') or '').strip()

    if not login or not password:
        return render_template('dating/register.html', error='Заполните все поля')

    password_hash = generate_password_hash(password)

    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM dating_users WHERE login=%s", (login,))
        else:
            cur.execute("SELECT id FROM dating_users WHERE login=?", (login,))
        if cur.fetchone():
            return render_template('dating/register.html', error='Логин уже существует')
        
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("INSERT INTO dating_users (login, password_hash) VALUES (%s, %s)", (login, password_hash))
        else:
            cur.execute("INSERT INTO dating_users (login, password_hash) VALUES (?, ?)", (login, password_hash))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('dating.login'))

@dating.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('dating/login.html')
    
    login_form = (request.form.get('login') or '').strip()
    password = (request.form.get('password') or '').strip()

    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT * FROM dating_users WHERE login=%s", (login_form,))
        else:
            cur.execute("SELECT * FROM dating_users WHERE login=?", (login_form,))
        user = cur.fetchone()
    finally:
        conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return render_template('dating/login.html', error='Неверный логин или пароль')

    session['user_id'] = user['id']
    session['login'] = user['login']
    return redirect(url_for('dating.profile'))

@dating.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dating.login'))

@dating.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('dating.login'))

    db_type = current_app.config.get('DB_TYPE')

    try:
        conn, cur = db_connect()
    except Exception as e:
        print("DB connection error:", e)
        return render_template('dating/profile.html', profile=None, error="Ошибка подключения к базе")

    try:
        if request.method == 'GET':
            # Получаем профиль текущего пользователя
            user_id = session['user_id']
            if db_type == 'postgres':
                cur.execute("SELECT * FROM dating_profiles WHERE user_id=%s", (user_id,))
            else:
                cur.execute("SELECT * FROM dating_profiles WHERE user_id=?", (user_id,))
            profile = cur.fetchone()
            return render_template('dating/profile.html', profile=profile)

        # POST — создание или обновление профиля
        full_name = (request.form.get('full_name') or '').strip()
        age = request.form.get('age')
        gender = (request.form.get('gender') or '').strip()
        search_gender = (request.form.get('search_gender') or '').strip()
        about = (request.form.get('about') or '').strip()

        # Валидация
        if not full_name or not age or gender not in GENDERS or search_gender not in GENDERS:
            return render_template('dating/profile.html', profile=request.form,
                                   error='Заполните все обязательные поля корректно')

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return render_template('dating/profile.html', profile=request.form,
                                   error='Возраст должен быть положительным числом')

        # Обработка фото
        photo_filename = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                photo_filename = secure_filename(photo.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                photo.save(os.path.join(UPLOAD_FOLDER, photo_filename))

        is_hidden_val = False if db_type == 'postgres' else 0

        # Проверяем, есть ли профиль текущего пользователя
        user_id = session['user_id']
        if db_type == 'postgres':
            cur.execute("SELECT id FROM dating_profiles WHERE user_id=%s", (user_id,))
        else:
            cur.execute("SELECT id FROM dating_profiles WHERE user_id=?", (user_id,))
        existing = cur.fetchone()

        if existing:
            # UPDATE существующего профиля
            if db_type == 'postgres':
                cur.execute("""
                    UPDATE dating_profiles
                    SET full_name=%s, age=%s, gender=%s, search_gender=%s, about=%s,
                        photo=COALESCE(%s, photo), is_hidden=%s
                    WHERE user_id=%s
                """, (full_name, age, gender, search_gender, about, photo_filename, is_hidden_val, user_id))
            else:
                cur.execute("""
                    UPDATE dating_profiles
                    SET full_name=?, age=?, gender=?, search_gender=?, about=?, photo=COALESCE(?, photo), is_hidden=?
                    WHERE user_id=?
                """, (full_name, age, gender, search_gender, about, photo_filename, is_hidden_val, user_id))
        else:
            # INSERT нового профиля с уникальным user_id
            if db_type == 'postgres':
                cur.execute("SELECT MAX(user_id) AS max_id FROM dating_profiles")
                row = cur.fetchone()
                max_id = row['max_id'] if row and row['max_id'] else 0
                new_user_id = max_id + 1
                cur.execute("""
                    INSERT INTO dating_profiles
                    (user_id, full_name, age, gender, search_gender, about, photo, is_hidden)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (new_user_id, full_name, age, gender, search_gender, about, photo_filename, is_hidden_val))
            else:
                cur.execute("SELECT MAX(user_id) AS max_id FROM dating_profiles")
                row = cur.fetchone()
                max_id = row['max_id'] if row and row['max_id'] else 0
                new_user_id = max_id + 1
                cur.execute("""
                    INSERT INTO dating_profiles
                    (user_id, full_name, age, gender, search_gender, about, photo, is_hidden)
                    VALUES (?,?,?,?,?,?,?,?)
                """, (new_user_id, full_name, age, gender, search_gender, about, photo_filename, is_hidden_val))

        conn.commit()
        return redirect(url_for('dating.profile'))

    except Exception as e:
        print("Profile error:", e)
        return render_template('dating/profile.html', profile=request.form, error="Произошла ошибка при сохранении профиля")

    finally:
        conn.close()


@dating.route('/profile/hide')
def hide_profile():
    if 'user_id' not in session:
        return abort(403)

    user_id = session['user_id']
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("UPDATE dating_profiles SET is_hidden=TRUE WHERE user_id=%s", (user_id,))
        else:
            cur.execute("UPDATE dating_profiles SET is_hidden=1 WHERE user_id=?", (user_id,))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('dating.profile'))

@dating.route('/delete_account')
def delete_account():
    if 'user_id' not in session:
        return abort(403)

    user_id = session['user_id']
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("DELETE FROM dating_users WHERE id=%s", (user_id,))
        else:
            cur.execute("DELETE FROM dating_users WHERE id=?", (user_id,))
        conn.commit()
    finally:
        conn.close()

    session.clear()
    return redirect(url_for('dating.register'))

@dating.route('/api/search')
def search():
    if 'user_id' not in session:
        return jsonify([])

    offset = int(request.args.get('offset', 0))
    name_filter = (request.args.get('name') or '').strip()
    age_min = request.args.get('age_min')
    age_max = request.args.get('age_max')

    user_id = session['user_id']
    conn, cur = db_connect()
    try:
        # текущий пользователь
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT gender, search_gender FROM dating_profiles WHERE user_id=%s", (user_id,))
        else:
            cur.execute("SELECT gender, search_gender FROM dating_profiles WHERE user_id=?", (user_id,))
        me = cur.fetchone()
        if not me:
            return jsonify([])

        # поиск
        query = "SELECT full_name, age, gender, about, photo FROM dating_profiles WHERE is_hidden=0 AND gender=%s AND search_gender=%s" if current_app.config.get('DB_TYPE') == 'postgres' else \
                "SELECT full_name, age, gender, about, photo FROM dating_profiles WHERE is_hidden=0 AND gender=? AND search_gender=?"
        params = [me['search_gender'], me['gender']]

        if name_filter:
            query += " AND full_name LIKE %s" if current_app.config.get('DB_TYPE') == 'postgres' else " AND full_name LIKE ?"
            params.append(f"%{name_filter}%")
        if age_min:
            query += " AND age >= %s" if current_app.config.get('DB_TYPE') == 'postgres' else " AND age >= ?"
            params.append(age_min)
        if age_max:
            query += " AND age <= %s" if current_app.config.get('DB_TYPE') == 'postgres' else " AND age <= ?"
            params.append(age_max)

        query += " LIMIT 3 OFFSET %s" if current_app.config.get('DB_TYPE') == 'postgres' else " LIMIT 3 OFFSET ?"
        params.append(offset)

        cur.execute(query, tuple(params) if current_app.config.get('DB_TYPE') == 'postgres' else params)
        results = [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()

    return jsonify(results)
