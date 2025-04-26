import os
from flask import Flask, redirect, render_template, request, session, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Reemplaza 'your_secret_key' con una clave segura

users = {}  # Diccionario temporal para almacenar usuarios (usa una base de datos en producción)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Verifica si los campos están vacíos
        if not username or not password:
            error = "Todos los campos son obligatorios"
            return render_template("register.html", error=error)
        
        # Verifica si el usuario ya existe
        if username in users:
            error = "El usuario ya existe"
            return render_template("register.html", error=error)
        
        # Guarda el usuario en el diccionario
        users[username] = password
        
        # Inicia sesión automáticamente
        session["user"] = username
        
        # Redirige al contenido del sitio web
        return redirect("/")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Verifica si el usuario existe y la contraseña es correcta
        if username in users and users[username] == password:
            session["user"] = username  # Guarda al usuario en la sesión
            return redirect("/")  # Redirige al contenido del sitio web
        else:
            error = "Usuario o contraseña incorrectos"
            return render_template("login.html", error=error)
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

@app.route("/variablesEjemplo")
def variablesEjemplo():
    return render_template('variablesEjemplo.html')

@app.route("/funcionesEjemplo")
def funcionesEjemplo():
    return render_template('funcionesEjemplo.html')

@app.route("/cEjemplo")
def cEjemplo():
    return render_template('cEjemplo.html')

@app.route("/logout")
def logout():
    session.pop("user", None)  # Elimina al usuario de la sesión
    flash("Has cerrado sesión correctamente", "info")
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
