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


@dating.route('/')
def index():
    return render_template('dating/index.html', authorized='user_id' in session, login=session.get('login'))


# @dating.route('/dev/fill_test_users')
# def fill_test_users():
#     if not current_app.debug:
#         abort(404)

#     test_users = [
#         ("user1", "123", "Андрей Косолапов", 23, "Мужской", "Женский", "Люблю спорт и реп.", "user1.jpg"),
#         ("user2", "123", "Настя Махмадбекова", 20, "Женский", "Мужской", "Люблю Imagine Dragons и Екатерину Шульман", "user2.jpg"),
#         ("user3", "123", "Виктор Белан", 43, "Мужской", "Женский", "Пою, снимаю тикток", "user3.jpg"),
#         ("user4", "123", "Анна Дзюба", 35, "Женский", "Мужской", "Царица", "user4.jpg"),
#         ("user5", "123", "Георгий Гергерт", 24, "Мужской", "Женский", "Бесы вышли, танцую джерси", "user5.jpg"),
#         ("user6", "123", "Ольга Бузова", 39, "Женский", "Мужской", "Кайфуйте! Жизнь одна!", "user6.jpg"),
#         ("user7", "123", "Игорь Харламов", 45, "Мужской", "Женский", "2 раза развелся", "user7.jpg"),
#         ("user8", "123", "Анна Новикова", 23, "Женский", "Мужской", "Ищу интересные знакомства.", "user8.jpg"),
#         ("user9", "123", "Никита Морозов", 22, "Мужской", "Женский", "Обожаю путешествовать и готовить.", "user9.jpg"),
#         ("user10", "123", "Елена Федорова", 21, "Женский", "Мужской", "Люблю животных и спорт.", "user10.jpg"),
#         ("user11", "123", "Владислав Васильев", 24, "Мужской", "Женский", "Путешествия и музыка — моя страсть.", "user11.jpg"),
#         ("user12", "123", "Ксения Михайлова", 22, "Женский", "Мужской", "Ищу друзей и новые впечатления.", "user12.jpg"),
#         ("user13", "123", "Максим Сидоров", 25, "Мужской", "Женский", "Люблю спорт и фильмы.", "user13.jpg"),
#         ("user14", "123", "Алина Егорова", 20, "Женский", "Мужской", "Обожаю книги и путешествия.", "user14.jpg"),
#         ("user15", "123", "Артур Николаев", 23, "Мужской", "Женский", "Ищу новые знакомства и друзей.", "user15.jpg"),
#         ("user16", "123", "София Орлова", 21, "Женский", "Мужской", "Музыка и спорт — моя жизнь.", "user16.jpg"),
#         ("user17", "123", "Константин Павлов", 26, "Мужской", "Женский", "Люблю готовить и путешествовать.", "user17.jpg"),
#         ("user18", "123", "Дарья Голубева", 22, "Женский", "Мужской", "Ищу интересных людей и друзей.", "user18.jpg"),
#         ("user19", "123", "Евгений Крылов", 24, "Мужской", "Женский", "Спорт, музыка и книги — мое хобби.", "user19.jpg"),
#         ("user20", "123", "Вероника Данилова", 23, "Женский", "Мужской", "Обожаю путешествия и животных.", "user20.jpg"),
#         ("user21", "123", "Андрей Тихонов", 25, "Мужской", "Женский", "Ищу новые впечатления и знакомства.", "user21.jpg"),
#         ("user22", "123", "Наталья Васильева", 20, "Женский", "Мужской", "Люблю спорт и книги.", "user22.jpg"),
#         ("user23", "123", "Роман Козлов", 22, "Мужской", "Женский", "Музыка, путешествия и друзья.", "user23.jpg"),
#         ("user24", "123", "Ирина Мартынова", 21, "Женский", "Мужской", "Обожаю кино и спорт.", "user24.jpg"),
#         ("user25", "123", "Денис Семёнов", 24, "Мужской", "Женский", "Люблю готовить и читать.", "user25.jpg"),
#         ("user26", "123", "Людмила Белова", 22, "Женский", "Мужской", "Путешествия и новые знакомства.", "user26.jpg"),
#         ("user27", "123", "Виктор Никитин", 23, "Мужской", "Женский", "Музыка, спорт и книги — моя жизнь.", "user27.jpg"),
#         ("user28", "123", "Татьяна Романова", 20, "Женский", "Мужской", "Люблю животных и путешествия.", "user28.jpg"),
#         ("user29", "123", "Игорь Морозов", 26, "Мужской", "Женский", "Ищу друзей и новые впечатления.", "user29.jpg"),
#         ("user30", "123", "Александра Петрова", 21, "Женский", "Мужской", "Музыка, спорт и кино — мои увлечения.", "user30.jpg"),
#     ]                                                           

#     conn, cur = db_connect()
#     db_type = current_app.config.get('DB_TYPE')

#     try:
#         for login, password, full_name, age, gender, search_gender, about, photo in test_users:
#             password_hash = generate_password_hash(password)

#             # ---------- USERS ----------
#             if db_type == 'postgres':
#                 cur.execute(
#                     "INSERT INTO dating_users (login, password_hash) VALUES (%s, %s) RETURNING id",
#                     (login, password_hash)
#                 )
#                 user_id = cur.fetchone()['id']
#             else:
#                 cur.execute(
#                     "INSERT INTO dating_users (login, password_hash) VALUES (?, ?)",
#                     (login, password_hash)
#                 )
#                 user_id = cur.lastrowid

#             # ---------- PROFILES ----------
#             if db_type == 'postgres':
#                 cur.execute("""
#                     INSERT INTO dating_profiles
#                     (user_id, full_name, age, gender, search_gender, about, photo, is_hidden)
#                     VALUES (%s,%s,%s,%s,%s,%s,%s,FALSE)
#                 """, (user_id, full_name, age, gender, search_gender, about, photo))
#             else:
#                 cur.execute("""
#                     INSERT INTO dating_profiles
#                     (user_id, full_name, age, gender, search_gender, about, photo, is_hidden)
#                     VALUES (?,?,?,?,?,?,?,0)
#                 """, (user_id, full_name, age, gender, search_gender, about, photo))

#         conn.commit()

#     finally:
    
#         conn.close()

#     return "OK"


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
        # Проверяем, существует ли логин
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM dating_users WHERE login=%s", (login,))
        else:
            cur.execute("SELECT id FROM dating_users WHERE login=?", (login,))
        if cur.fetchone():
            return render_template('dating/register.html', error='Логин уже существует')

        # Вставляем нового пользователя и получаем его ID
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "INSERT INTO dating_users (login, password_hash) VALUES (%s, %s) RETURNING id",
                (login, password_hash)
            )
            new_id = cur.fetchone()['id']
        else:
            cur.execute(
                "INSERT INTO dating_users (login, password_hash) VALUES (?, ?)",
                (login, password_hash)
            )
            new_id = cur.lastrowid

        conn.commit()
        session['user_id'] = new_id
        session['login'] = login

    finally:
        conn.close()

    return redirect(url_for('dating.profile'))


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

    user_id = session['user_id']
    db_type = current_app.config.get('DB_TYPE')
    conn, cur = db_connect()

    try:
        if request.method == 'GET':
            # Получаем профиль текущего пользователя
            if db_type == 'postgres':
                cur.execute("SELECT * FROM dating_profiles WHERE user_id=%s", (user_id,))
            else:
                cur.execute("SELECT * FROM dating_profiles WHERE user_id=?", (user_id,))
            profile = cur.fetchone()
            return render_template('dating/profile.html', profile=profile)

        # POST — создаём или обновляем профиль
        full_name = (request.form.get('full_name') or '').strip()
        age = request.form.get('age')
        gender = (request.form.get('gender') or '').strip()
        search_gender = (request.form.get('search_gender') or '').strip()
        about = (request.form.get('about') or '').strip()

        if not full_name or not age or gender not in GENDERS or search_gender not in GENDERS:
            return render_template('dating/profile.html', profile=request.form,
                                   error='Заполните все обязательные поля корректно')

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except:
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

        # Проверяем, есть ли уже профиль
        if db_type == 'postgres':
            cur.execute("SELECT id FROM dating_profiles WHERE user_id=%s", (user_id,))
        else:
            cur.execute("SELECT id FROM dating_profiles WHERE user_id=?", (user_id,))
        existing = cur.fetchone()

        if existing:
            # Обновляем профиль
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
            # Создаём новый профиль
            if db_type == 'postgres':
                cur.execute("""
                    INSERT INTO dating_profiles
                    (user_id, full_name, age, gender, search_gender, about, photo, is_hidden)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (user_id, full_name, age, gender, search_gender, about, photo_filename, is_hidden_val))
            else:
                cur.execute("""
                    INSERT INTO dating_profiles
                    (user_id, full_name, age, gender, search_gender, about, photo, is_hidden)
                    VALUES (?,?,?,?,?,?,?,?)
                """, (user_id, full_name, age, gender, search_gender, about, photo_filename, is_hidden_val))

        conn.commit()
        return redirect(url_for('dating.search_page'))

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
        return jsonify({'error': 'Вы не авторизованы', 'results': []})

    def to_int(val):
        try:
            return int(val)
        except (TypeError, ValueError):
            return None

    offset = to_int(request.args.get('offset')) or 0
    name_filter = (request.args.get('name') or '').strip()
    age_min = to_int(request.args.get('age_min'))
    age_max = to_int(request.args.get('age_max'))

    user_id = session['user_id']
    conn, cur = db_connect()

    try:
        # Получаем профиль текущего пользователя
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "SELECT gender, search_gender FROM dating_profiles WHERE user_id=%s",
                (user_id,)
            )
        else:
            cur.execute(
                "SELECT gender, search_gender FROM dating_profiles WHERE user_id=?",
                (user_id,)
            )

        me = cur.fetchone()
        if not me:
            return jsonify({'error': 'Сначала заполните свой профиль', 'results': []})

        # Базовый запрос: ищем подходящих пользователей, исключая текущего
        if current_app.config.get('DB_TYPE') == 'postgres':
            query = """
                SELECT full_name, age, gender, about, photo
                FROM dating_profiles
                WHERE is_hidden = FALSE
                  AND gender = %s
                  AND search_gender = %s
                  AND user_id != %s
            """
        else:
            query = """
                SELECT full_name, age, gender, about, photo
                FROM dating_profiles
                WHERE is_hidden = 0
                  AND gender = ?
                  AND search_gender = ?
                  AND user_id != ?
            """

        params = [me['search_gender'], me['gender'], user_id]

        # Фильтр по имени
        if name_filter:
            if current_app.config.get('DB_TYPE') == 'postgres':
                query += " AND full_name ILIKE %s"
            else:
                query += " AND full_name LIKE ?"
            params.append(f"%{name_filter}%")

        # Фильтр по возрасту
        if age_min is not None:
            query += " AND age >= %s" if current_app.config.get('DB_TYPE') == 'postgres' else " AND age >= ?"
            params.append(age_min)

        if age_max is not None:
            query += " AND age <= %s" if current_app.config.get('DB_TYPE') == 'postgres' else " AND age <= ?"
            params.append(age_max)

        # LIMIT/OFFSET
        if current_app.config.get('DB_TYPE') == 'postgres':
            query += " ORDER BY id LIMIT %s OFFSET %s"
        else:
            query += " ORDER BY user_id LIMIT ? OFFSET ?"

        params.append(3)  # limit
        params.append(offset)

        cur.execute(query, tuple(params) if current_app.config.get('DB_TYPE') == 'postgres' else params)
        results = [dict(r) for r in cur.fetchall()]

        if not results:
            return jsonify({'error': 'Пользователи, подходящие по вашим критериям, не найдены.', 'results': []})

        return jsonify({'results': results, 'error': None})

    finally:
        conn.close()


@dating.route('/search')
def search_page():
    if 'user_id' not in session:
        return redirect(url_for('dating.login'))
    return render_template('dating/search.html')
