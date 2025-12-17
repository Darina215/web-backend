from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
import random

lab9 = Blueprint("lab9", __name__, template_folder="templates")

# Хранилище подарков на сервере (ОБЩЕЕ)
GIFTS = []

USERS = {}

MESSAGES = [
    "С Новым годом! Пусть в новом году сбудутся все мечты!",
    "Желаем счастья, здоровья и благополучия!",
    "Пусть каждый день будет наполнен радостью!",
    "Успехов в учёбе и новых достижений!",
    "Пусть Новый год принесёт только хорошее!",
    "Желаем тепла, уюта и гармонии!",
    "Пусть удача всегда будет рядом!",
    "Исполнения самых заветных желаний!",
    "Счастья, улыбок и хорошего настроения!",
    "Пусть этот год станет для вас лучшим!"
]

def init_gifts():
    global GIFTS
    if GIFTS:
        return

    positions = [
        (10, 20), (10, 40), (10, 60), (10, 80),
        (40, 30), (40, 50), (40, 70),
        (70, 20), (70, 40), (70, 60)
    ]

    for i in range(10):
        top, left = positions[i]

        GIFTS.append({
            "id": i,
            "opened": False,
            "top": top,
            "left": left,
            "box": f"box{i+1}.jpg",
            "gift": f"gift{i+1}.jpg",
            "message": MESSAGES[i],
            "require_auth": i >= 5
        })


@lab9.route("/lab9/")
def index():
    init_gifts()
    return render_template(
        "lab9/index.html",
        gifts=GIFTS,
        opened=session.get("opened", 0),
        remaining=sum(not g["opened"] for g in GIFTS),
        is_auth="user" in session,
        login=session.get("user")
    )

@lab9.route("/open", methods=["POST"])
def open_gift():
    data = request.json
    gift_id = data.get("id")

    if gift_id is None:
        return jsonify({"error": "Некорректный запрос"})

    gift = GIFTS[gift_id]

    if gift["opened"]:
        return jsonify({"error": "Этот подарок уже забрали 🎁"})

    if session.get("opened", 0) >= 3:
        return jsonify({"error": "Можно открыть не более 3 подарков"})

    if gift["require_auth"] and "user" not in session:
        return jsonify({"error": "Подарок доступен только авторизованным"})

    gift["opened"] = True
    session["opened"] = session.get("opened", 0) + 1

    return jsonify({
        "ok": True,
        "message": gift["message"],
        "image": gift["gift"],
        "opened": session["opened"],
        "remaining": sum(not g["opened"] for g in GIFTS)
    })

@lab9.route("/reset", methods=["POST"])
def reset():
    if "user" not in session:
        return jsonify({"error": "Нет доступа"})

    for g in GIFTS:
        g["opened"] = False

    session["opened"] = 0
    return jsonify({"ok": True})

@lab9.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if USERS.get(request.form["login"]) == request.form["password"]:
            session["user"] = request.form["login"]
            return redirect(url_for("lab9.index"))
    return render_template("lab9/login.html")

@lab9.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        USERS[request.form["login"]] = request.form["password"]
        return redirect(url_for("lab9.login"))
    return render_template("lab9/register.html")

@lab9.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("lab9.index"))
