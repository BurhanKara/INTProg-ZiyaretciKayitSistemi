from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Model tanımı
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

def export_users_to_json():
    with app.app_context():
        users = User.query.all()
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'password': user.password  # Hashlenmiş şifre veritabanında saklanıyor varsayımıyla
            })

        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Kullanıcılar başarıyla users.json dosyasına kaydedildi!")

if __name__ == '__main__':
    export_users_to_json()
