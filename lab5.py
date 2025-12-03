from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] =='postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'darina_redkacheva_knowledge_base',
            user = 'darina_redkacheva_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()
    
@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                                error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);",
                (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);",
                (login, password_hash, real_name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login = ?;", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
    
    if not check_password_hash(user["password"], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')
    
    session['login'] = login

    db_close(conn, cur)

    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = True if request.form.get('is_favorite') else False
    is_public = True if request.form.get('is_public') else False

    #Добавление валидации
    if not title or not article_text:
        return render_template('lab5/create_article.html', 
                             error='Заполните название и текст статьи')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("INSERT INTO articles(login_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);",
        (login_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("INSERT INTO articles(login_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);",
        (login_id, title, article_text, is_favorite, is_public))

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC, id;", (login_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC, id;", (login_id,))
    articles = cur.fetchall()

    db_close(conn, cur)

     # Проверка на отсутствие статей
    if not articles:
        return render_template('/lab5/articles.html', 
                             articles=articles, 
                             no_articles=True)

    return render_template('/lab5/articles.html', articles=articles, no_articles=False)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Получаем пользователя
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user['id']
    
    # Проверяем, принадлежит ли статья пользователю
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND login_id=%s;", 
                   (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?;", 
                   (article_id, user_id))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                             article=article)
    
    # Обработка POST запроса (сохранение изменений)
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = True if request.form.get('is_favorite') else False
    is_public = True if request.form.get('is_public') else False
    
    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                             article=article,
                             error='Заполните название и текст статьи')
    
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s WHERE id=%s;",
                   (title, article_text, is_favorite, is_public, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=? WHERE id=?;",
                   (title, article_text, is_favorite, is_public, article_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Получаем пользователя
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user['id']
    
    # Проверяем, принадлежит ли статья пользователю
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND login_id=%s;", 
                   (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?;", 
                   (article_id, user_id))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')

    # Удаляем статью
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))
    
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/all_users')
def all_users():
    """Страница со всеми зарегистрированными пользователями"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT login, real_name FROM users;")
    else:
        cur.execute("SELECT login, real_name FROM users;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/all_users.html', users=users)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    """Страница смены имени и пароля"""
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] =='postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)
    
    # Обработка формы
    real_name = request.form.get('real_name')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Получаем текущего пользователя
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    errors = []
    
    # Проверяем, хочет ли пользователь сменить пароль
    if old_password or new_password or confirm_password:
        if not check_password_hash(user['password'], old_password):
            errors.append('Неверный старый пароль')
        elif new_password != confirm_password:
            errors.append('Новый пароль и подтверждение не совпадают')
        elif not new_password:
            errors.append('Новый пароль не может быть пустым')
        else:
            # Хешируем новый пароль
            new_password_hash = generate_password_hash(new_password)
            if current_app.config['DB_TYPE'] =='postgres':
                cur.execute("UPDATE users SET password=%s WHERE login=%s;", (new_password_hash, login))
            else:
                cur.execute("UPDATE users SET password=? WHERE login=?;", (new_password_hash, login))
    
    # Обновляем реальное имя
    if real_name != user['real_name']:
        if current_app.config['DB_TYPE'] =='postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?;", (real_name, login))
    
    if errors:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, errors=errors)
    
    db_close(conn, cur)
    return redirect('/lab5/profile')


@lab5.route('/lab5/public_articles')
def public_articles():
    """Публичные статьи для всех пользователей"""
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] =='postgres':
        cur.execute("SELECT articles.*, users.login as author_login, users.real_name as author_name FROM articles JOIN users ON articles.login_id = users.id WHERE articles.is_public = true ORDER BY articles.is_favorite DESC, articles.id;")
    else:
        cur.execute("SELECT articles.*, users.login as author_login, users.real_name as author_name FROM articles JOIN users ON articles.login_id = users.id WHERE articles.is_public = 1 ORDER BY articles.is_favorite DESC, articles.id;")
    
    articles = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/public_articles.html', articles=articles)