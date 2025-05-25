from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User modeli sadece bir kez tanımlanmalı
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer, default=0)  # 0: normal kullanıcı, 1: admin
    comments = db.relationship('Comment', backref='user', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Admin kontrolü için decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 1:
            abort(403)  # Yetkisiz erişim
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')


# Giriş yapma
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('E-posta veya şifre hatalı!', 'danger')
    return render_template('login.html')


# Kayıt olma
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


# Yönetici paneli - kullanıcıları listele
@app.route('/admin')
@admin_required
def admin_panel():
    users = User.query.all()
    return render_template('admin.html', users=users)


# Kullanıcı silme
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Kendi hesabınızı silemezsiniz!", "danger")
        return redirect(url_for('admin_panel'))
    db.session.delete(user)
    db.session.commit()
    flash("Kullanıcı başarıyla silindi.", "success")
    return redirect(url_for('admin_panel'))


# Kullanıcı rol değiştirme
@app.route('/admin/change_role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role not in ['0', '1']:
        flash("Geçersiz rol seçimi.", "danger")
        return redirect(url_for('admin_panel'))
    user.role = int(new_role)
    db.session.commit()
    flash("Kullanıcı rolü güncellendi.", "success")
    return redirect(url_for('admin_panel'))


# Kullanıcı şifre değiştirme
@app.route('/admin/change_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def change_password(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_password = request.form.get('password')
        if not new_password:
            flash("Şifre boş olamaz.", "danger")
            return redirect(url_for('change_password', user_id=user.id))
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        flash("Şifre başarıyla değiştirildi.", "success")
        return redirect(url_for('admin_panel'))
    return render_template('change_password.html', user=user)


# Kullanıcı paneli / dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)


# Çıkış yapma
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# İletişim sayfası
@app.route('/iletisim')
def iletisim():
    return render_template('iletisim.html')


# Destek sayfası
@app.route('/destek')
def destek():
    return render_template('destek.html')


# Hakkımızda sayfası
@app.route('/hakkimizda.html')
def hakkimizda():
    return render_template('hakkimizda.html')


# Yorumlar sayfası
@app.route('/yorumlar')
@login_required
def yorumlar():
    yorumlar = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('yorumlar.html', yorumlar=yorumlar)


# Yorum yapma sayfası
@app.route('/yorum_yap.html', methods=['GET', 'POST'])
@login_required
def yorum_yap():
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash("Yorum boş bırakılamaz.", 'danger')
            return redirect(url_for('yorum_yap'))

        new_comment = Comment(user_id=current_user.id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        flash("Yorumunuz başarıyla eklendi!", 'success')
        return redirect(url_for('yorum_yap'))

    yorumlar = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('yorum_yap.html', yorumlar=yorumlar)


# Yorum silme
@app.route('/yorum_sil/<int:yorum_id>')
@login_required
def yorum_sil(yorum_id):
    yorum = Comment.query.get_or_404(yorum_id)
    if yorum.user_id != current_user.id:
        flash("Bu yorumu silemezsiniz!", 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(yorum)
    db.session.commit()
    flash("Yorum silindi.", 'success')
    return redirect(url_for('yorum_yap'))


# Yorum düzenleme
@app.route('/yorum_duzenle/<int:yorum_id>', methods=['GET', 'POST'])
@login_required
def yorum_duzenle(yorum_id):
    yorum = Comment.query.get_or_404(yorum_id)
    if yorum.user_id != current_user.id:
        flash("Bu yorumu düzenleyemezsiniz!", 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        yeni_icerik = request.form.get('content')
        yorum.content = yeni_icerik
        db.session.commit()
        flash("Yorum güncellendi!", 'success')
        return redirect(url_for('yorum_yap'))

    return render_template('yorum_duzenle.html', yorum=yorum)


# Sipariş sayfası
@app.route('/siparis.html')
def siparis():
    return render_template('siparis.html')


# Restoran menüsü (örnek içerik eklendi)
@app.route('/restoran')
def restoran():
    menu_items = [
        {"kategori": "Çorbalar", "items": ["Mercimek Çorbası", "Tarhana Çorbası"]},
        {"kategori": "Ana Yemekler", "items": ["Kuru Fasulye", "Tavuk Sote"]}
    ]
    return render_template('restoran.html', menu=menu_items)


# Admin paneli detay sayfası
@app.route('/admin_paneli')
@login_required
@admin_required
def admin_paneli():
    return render_template('admin_paneli.html')


#if __name__ == '__main__':
#    with app.app_context():
#        db.create_all()
#    app.run(debug=True)

import os
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
