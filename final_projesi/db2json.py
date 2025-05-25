from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Kullanıcı modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Yorum modeli
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Tarih eklendi

    user = db.relationship('User', backref='comments')

# Yorumları JSON dosyasına aktar
def export_comments_to_json():
    with app.app_context():
        comments = Comment.query.order_by(Comment.created_at.desc()).all()
        data = []
        for comment in comments:
            data.append({
                'id': comment.id,
                'user_id': comment.user_id,
                'user_name': comment.user.name,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        with open('yorumlar.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("✅ Yorumlar başarıyla yorumlar.json dosyasına kaydedildi!")

if __name__ == '__main__':
    export_comments_to_json()
