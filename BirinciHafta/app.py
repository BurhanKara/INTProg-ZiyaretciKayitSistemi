from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/yorum/yap')
def yorum_yap():
    return render_template('yorum_yap.html')

@app.route('/destek')
def destek():
    return render_template('destek.html')

@app.route('/iletisim')
def iletisim():
    return render_template('iletisim.html')

@app.route('/hakkimizda')
def hakkimizda():
    return render_template('hakkimizda.html')

@app.route('/yorum/duzenle/<int:id>')
def yorum_duzenle(id):
    return render_template('yorum_duzenle.html')

if __name__ == '__main__':
    app.run(debug=True) 