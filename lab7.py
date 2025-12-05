from flask import Blueprint, render_template, request, abort, jsonify, current_app
from datetime import datetime
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)


def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='darina_redkacheva_knowledge_base',
            user='darina_redkacheva_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "films.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def row_to_dict(row):
    if isinstance(row, dict):
        return row
    return {
        "id": row["id"],
        "title": row["title"],
        "title_ru": row["title_ru"],
        "year": row["year"],
        "description": row["description"]
    }


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()

    cur.execute("SELECT * FROM films ORDER BY id;")
    rows = cur.fetchall()

    films = [row_to_dict(r) for r in rows]

    conn.close()
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        abort(404)

    return jsonify(row_to_dict(row))


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT id FROM films WHERE id = ?;", (id,))

    if not cur.fetchone():
        conn.close()
        abort(404)

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ?;", (id,))

    conn.commit()
    conn.close()

    return '', 204


def validate(film):
    current_year = datetime.now().year

    if not film.get('title_ru', '').strip():
        return {"title_ru": "Русское название обязательно"}, False

    try:
        year = int(film.get("year", 0))
        if year < 1895 or year > current_year:
            return {"year": f"Год должен быть 1895–{current_year}"}, False
    except:
        return {"year": "Год должен быть числом"}, False

    if not film.get('description', '').strip():
        return {"description": "Описание обязательно"}, False

    if len(film['description']) > 2000:
        return {"description": "Описание ≤ 2000 символов"}, False

    if not film.get("title", "").strip():
        film["title"] = film["title_ru"]

    return film, True


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT id FROM films WHERE id = ?;", (id,))

    if not cur.fetchone():
        conn.close()
        abort(404)

    film = request.get_json()
    validated, ok = validate(film)
    if not ok:
        conn.close()
        return validated, 400

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            UPDATE films 
            SET title=%s, title_ru=%s, year=%s, description=%s 
            WHERE id=%s 
            RETURNING *;
        """, (validated['title'], validated['title_ru'], validated['year'], validated['description'], id))
        updated = cur.fetchone()
    else:
        cur.execute("""
            UPDATE films 
            SET title=?, title_ru=?, year=?, description=? 
            WHERE id=?;
        """, (validated['title'], validated['title_ru'], validated['year'], validated['description'], id))
        conn.commit()

        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
        updated = row_to_dict(cur.fetchone())

    conn.commit()
    conn.close()
    return jsonify(row_to_dict(updated))


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    validated, ok = validate(film)
    if not ok:
        return validated, 400

    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (validated['title'], validated['title_ru'], validated['year'], validated['description']))
        new_id = cur.fetchone()['id']
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?);
        """, (validated['title'], validated['title_ru'], validated['year'], validated['description']))
        new_id = cur.lastrowid

    conn.commit()
    conn.close()

    return jsonify({"id": new_id}), 201


