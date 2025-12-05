from flask import Blueprint, render_template, request, session, abort, current_app, jsonify
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

# -----------------------------
# ФУНКЦИИ РАБОТЫ С БАЗОЙ
# -----------------------------
def db_connect():
    return psycopg2.connect(
        host='localhost',
        database='darina_redkacheva_knowledge_base',
        user='darina_redkacheva_knowledge_base',
        password='123'   # замени на свой пароль!
    )

def db_close(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


# -----------------------------
# ГЛАВНАЯ СТРАНИЦА ЛАБОРАТОРНОЙ
# -----------------------------
@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


# -----------------------------
# GET /lab7/rest-api/films/
# -----------------------------
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = db_connect()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM films ORDER BY id;")
    films = cursor.fetchall()

    db_close(conn, cursor)
    return jsonify(films)


# -----------------------------
# GET /lab7/rest-api/films/<id>
# -----------------------------
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = db_connect()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM films WHERE id = %s;", (id,))
    film = cursor.fetchone()

    db_close(conn, cursor)

    if film is None:
        abort(404)

    return jsonify(film)


# -----------------------------
# DELETE /lab7/rest-api/films/<id>
# -----------------------------
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM films WHERE id = %s;", (id,))
    if cursor.fetchone() is None:
        db_close(conn, cursor)
        abort(404)

    cursor.execute("DELETE FROM films WHERE id = %s;", (id,))
    db_close(conn, cursor)

    return '', 204


# -----------------------------
# PUT /lab7/rest-api/films/<id>
# -----------------------------
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn = db_connect()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Проверяем, что фильм существует
    cursor.execute("SELECT * FROM films WHERE id = %s;", (id,))
    old = cursor.fetchone()
    if old is None:
        db_close(conn, cursor)
        abort(404)

    film = request.get_json()
    current_year = datetime.now().year

    # Валидации
    if not film.get('title_ru', '').strip():
        db_close(conn, cursor)
        return {'title_ru': 'Русское название обязательно для заполнения'}, 400

    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            db_close(conn, cursor)
            return {'year': f'Год должен быть в диапазоне от 1895 до {current_year}'}, 400
    except:
        db_close(conn, cursor)
        return {'year': 'Год должен быть числом'}, 400

    description = film.get('description', '').strip()
    if not description:
        db_close(conn, cursor)
        return {'description': 'Заполните описание'}, 400
    if len(description) > 2000:
        db_close(conn, cursor)
        return {'description': 'Описание не должно превышать 2000 символов'}, 400

    # Если нет оригинального названия — копируем русское
    if not film.get('title', '').strip():
        film['title'] = film['title_ru']

    # Обновление в БД
    cursor.execute("""
        UPDATE films
        SET title = %s, title_ru = %s, year = %s, description = %s
        WHERE id = %s
        RETURNING *;
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))

    updated = cursor.fetchone()
    db_close(conn, cursor)

    return jsonify(updated)


# -----------------------------
# POST /lab7/rest-api/films/
# -----------------------------
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    current_year = datetime.now().year

    # Валидация
    if not film.get('title_ru', '').strip():
        return {'title_ru': 'Русское название обязательно'}, 400

    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            return {'year': f'Год должен быть в диапазоне от 1895 до {current_year}'}, 400
    except:
        return {'year': 'Год должен быть числом'}, 400

    description = film.get('description', '').strip()
    if not description:
        return {'description': 'Заполните описание'}, 400
    if len(description) > 2000:
        return {'description': 'Описание не должно превышать 2000 символов'}, 400

    if not film.get('title', '').strip():
        film['title'] = film['title_ru']

    # Запись в БД
    conn = db_connect()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO films (title, title_ru, year, description)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (film['title'], film['title_ru'], film['year'], film['description']))

    new_id = cursor.fetchone()['id']
    db_close(conn, cursor)

    return jsonify({"id": new_id}), 201




