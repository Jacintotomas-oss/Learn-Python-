import os
from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Genera una clave secreta segura

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Inicializa la base de datos

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada usuario
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario
    password = db.Column(db.String(120), nullable=False)  # Contraseña

users = {}  # Diccionario temporal para almacenar usuarios (usa una base de datos en producción)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Verifica si los campos están vacíos
        if not username or not password:
            flash("Todos los campos son obligatorios", "danger")
            return redirect("/register")
        
        # Verifica si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El usuario ya existe", "danger")
            return redirect("/register")
        
        # Cifra la contraseña antes de guardarla
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Guarda el usuario en la base de datos
        new_user = User(username=username, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        
        # Mensaje de éxito
        flash("Cuenta creada exitosamente. Ahora puedes iniciar sesión.", "success")
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Verifica si el usuario existe y la contraseña es correcta
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session["user"] = username  # Guarda al usuario en la sesión
            flash("Inicio de sesión exitoso", "success")  # Mensaje flash de éxito
            return redirect("/")  # Redirige al contenido del sitio web
        else:
            flash("Usuario o contraseña incorrectos", "danger")  # Mensaje flash de error
            return redirect("/login")
    return render_template("login.html")

@app.route('/')
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return redirect("/register")  # Redirige a la página de registro si no hay sesión

@app.route('/variables')
def variables():
    if "user" not in session:
        return redirect("/register")  # Redirige al registro si no está autenticado
    return render_template('variables.html')

@app.route('/funciones')
def funciones():
    if "user" not in session:
        return redirect("/register")
    return render_template('funciones.html')

@app.route('/condicionales')
def condicionales():
    if "user" not in session:
        return redirect("/register")
    return render_template('condicionales.html')

@app.route("/ciclos")
def ciclos():
    if "user" not in session:
        return redirect("/register")
    return render_template('ciclos.html')

@app.route("/listas")
def listas():
    if "user" not in session:
        return redirect("/register")
    return render_template("listas.html")

@app.route("/OL")
def OL():
    if "user" not in session:
        return redirect("/register")
    return render_template("OL.html")

@app.route("/variablesEjemplo")
def variablesEjemplo():
    return render_template('variablesEjemplo.html')

@app.route("/funcionesEjemplo")
def funcionesEjemplo():
    return render_template('funcionesEjemplo.html')

@app.route("/cEjemplo")
def cEjemplo():
    return render_template('cEjemplo.html')

@app.route("/ciclosEjemplo")
def ciclosEjemplo():
    return render_template('ciclosEjemplo.html')

@app.route("/listasEjemplo")
def listasEjemplo():
    return render_template('listasEjemplo.html')

@app.route("/OLEjemplo")
def OLEjemplo():
    return render_template('OLEjemplo.html')

@app.route('/OLejemplos')
def operadores_logicos_ejemplos():
    return render_template('OLejemplos.html')

@app.route("/logout")
def logout():
    session.pop("user", None)  # Elimina al usuario de la sesión
    flash("Has cerrado sesión correctamente", "info")
    return redirect("/login")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True, host='0.0.0.0', port=5000)
