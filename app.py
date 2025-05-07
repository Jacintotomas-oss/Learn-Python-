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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Verifica si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El usuario ya existe. Intenta con otro nombre de usuario.", "danger")
            return redirect("/register")
        
        # Crea un nuevo usuario
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect("/login")
    
    return render_template("register.html")  # Renderiza directamente el archivo register.html

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Verifica si el usuario existe
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session["user"] = username  # Guarda al usuario en la sesión
            flash("Inicio de sesión exitoso.", "success")
            return redirect("/")
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
            return redirect("/login")
    
    return render_template("login.html")  # Renderiza directamente el archivo login.html

@app.route('/')
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return redirect("/register")  # Redirige a la página de registro si no hay sesión

@app.route("/logout")
def logout():
    session.pop("user", None)  # Elimina al usuario de la sesión
    flash("Has cerrado sesión correctamente", "info")
    return redirect("/login")

#ruta de las paginas de teorias 

@app.route('/variables')
def variables():
    if "user" not in session:
        return redirect("/register")  # Redirige al registro si no está autenticado
    return render_template('variables.html')

@app.route('/condicionales')
def condicionales():
    if "user" not in session:
        return redirect("/register")
    return render_template("condicionales.html")

@app.route ("/funciones")
def funciones():
    if "user" not in session:
        return redirect("/register")
    return render_template("funciones.html")

@app.route ("/ciclos")
def ciclos():
    if "user" not in session:
        return redirect("/register")
    return render_template("ciclos.html")

@app.route("/listas")
def listas():
    if "user" not in session:
        return redirect("/register")
    return render_template("listas.html")

@app.route("/OL")
def OL():
    if "user" not in session :
        return redirect("/register")
    return render_template("OL.html")

@app.route("/diccionario")
def diccionario():
    if "user" not in session:
        return redirect("/register")
    return render_template("diccionario.html")

#Ruta de las paginas de ejercicios

@app.route("/variablesEjemplo")
def variablesEjemplo():
    if "user" not in session: 
        return redirect("/register")
    return render_template("variablesEjemplo.html")

@app.route("/cEjemplo")
def cEjemplo():
    if "user" not in session:
        return redirect("/register")
    return render_template("cEjemplo.html")

@app.route("/funcionesEjemplo")
def funcionesEjemplo():
    if "user" not in session:
        return redirect("/register")
    return render_template("funcionesEjemplo.html")

@app.route("/ciclosEjemplo")
def ciclosEjemplo():
    if "user" not in session:
        return redirect("/register")
    return render_template("ciclosEjemplo.html")

@app.route("/listasEjemplo")
def listasEjemplo():
    if "user" not in session:
        return redirect("/register")
    return render_template("listasEjemplo.html")

@app.route("/Dejemplos")
def Dejemplos():
    if "user" not in session:
        return redirect("/register")
    return render_template("Dejemplos.html")

@app.route("/OLejemplos")
def OLejemplos():
    if "user" not in session:
        return redirect("/register")
    return render_template("OLejemplos.html")


    
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True, host='0.0.0.0', port=5000)
