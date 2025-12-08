from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_, func

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not login_form.strip():
        return render_template('lab8/register.html',
                               error='Имя пользователя не может быть пустым')

    if not password_form or not password_form.strip():
        return render_template('lab8/register.html',
                               error='Пароль не может быть пустым')
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me') == 'on'
    
    if not login_form or not login_form.strip():
        return render_template('lab8/login.html',
                               error='Имя пользователя не может быть пустым')

    if not password_form or not password_form.strip():
        return render_template('lab8/login.html',
                               error='Пароль не может быть пустым')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=False)
            return redirect('/lab8/')
    
    return render_template('/lab8/login.html',
                           error = 'Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
def article_list():
    if current_user.is_authenticated:
        user_articles = articles.query.filter_by(login_id=current_user.id).all()
    else:
        user_articles = articles.query.filter_by(is_public=True).all()

    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    text = request.form.get('text')
    is_public = request.form.get('is_public') == 'on'

    if not title or not title.strip():
        return render_template('lab8/create.html',
                               error="Название статьи не может быть пустым")

    if not text or not text.strip():
        return render_template('lab8/create.html',
                               error="Текст статьи не может быть пустым")

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=text,
        is_favorite=False,
        is_public=is_public,
        likes=0
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/articles/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    text = request.form.get('text')
    is_public = request.form.get('is_public') == 'on'

    if not title or not title.strip():
        return render_template('lab8/edit_article.html',
                               article=article,
                               error="Название не может быть пустым")

    if not text or not text.strip():
        return render_template('lab8/edit_article.html',
                               article=article,
                               error="Текст не может быть пустым")

    article.title = title
    article.article_text = text
    article.is_public = is_public

    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/articles/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)

    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/articles/search', methods=['GET', 'POST'])
def search_articles():
    query = request.form.get('query', '').strip()

    if not query:
        return redirect('/lab8/articles/')

    # Если авторизован — свои + публичные чужие
    if current_user.is_authenticated:
        articles_list = articles.query.filter(
            or_(
                articles.login_id == current_user.id,
                articles.is_public == True
            ),
            func.lower(articles.title).like(f"%{query.lower()}%") |
            func.lower(articles.article_text).like(f"%{query.lower()}%")
        ).all()
    else:
        # Неавторизованные — только публичные
        articles_list = articles.query.filter(
            articles.is_public == True,
            func.lower(articles.title).like(f"%{query.lower()}%") |
            func.lower(articles.article_text).like(f"%{query.lower()}%")
        ).all()

    return render_template('lab8/articles.html', articles=articles_list)