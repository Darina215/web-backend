from app import app
from db import db
from dating.models import DatingUser

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Таблицы успешно созданы")
