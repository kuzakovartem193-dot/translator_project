from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    source_text = db.Column(db.Text)
    translated_text = db.Column(db.Text)
    from_lang = db.Column(db.String(10))
    to_lang = db.Column(db.String(10))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создаем таблицы сразу при старте
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    translated = ""
    if request.method == "POST":
        text = request.form.get("text")
        from_lang = request.form.get("from_lang")
        to_lang = request.form.get("to_lang")
        translated = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
        db.session.add(History(user_id=current_user.id,
                               source_text=text,
                               translated_text=translated,
                               from_lang=from_lang,
                               to_lang=to_lang))
        db.session.commit()
    history = History.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", translated=translated, history=history)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        if not User.query.filter_by(username=username).first():
            db.session.add(User(username=username, password=password))
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
