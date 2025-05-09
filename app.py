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

# Clase para las preguntas del quizz
class Pregunta:
    p_id = 0
    pregunta = ''
    opcion1 = ''
    opcion2 = ''
    opcion3 = ''
    respuestaCorrecta = 0

    def __init__(self, p_id, Pregunta, opcion1, opcion2, opcion3, respuestaCorrecta):
        self.p_id = p_id
        self.pregunta = Pregunta
        self.opcion1 = opcion1
        self.opcion2 = opcion2
        self.opcion3 = opcion3
        self.respuestaCorrecta = respuestaCorrecta

    def Respuesta_Correcta(self):
        if self.respuestaCorrecta == 1:
            return self.opcion1
        elif self.respuestaCorrecta == 2:
            return self.opcion2
        elif self.respuestaCorrecta == 3:
            return self.opcion3

# Lista de preguntas
P1 = Pregunta(1, "¿Cual NO es un bucle en programacion?", "For", "While", "If", 3)
P2 = Pregunta(2, "¿Cual es el lenguaje de programacion mas utilizado?", "Python", "Java", "C++",  1)
P3 = Pregunta(3, "¿Cual de las siguientes es una cadena de texto?", "String", "Int", "Float", 1)
P4 = Pregunta(4, "¿Cual de los siguiente es un condicional?", "If", "For", "While", 1)
P5 = Pregunta(5, "¿Cual de los siguiente es un bucle?", "If", "For", "Switch", 2)
P6 = Pregunta(6, "¿Que es un ciclo?", "Un bucle", "Una condicion", "Una variable", 1)
P7 = Pregunta(7, "¿Cual de las siguientes es una funcion?", "Print", "If", "For", 1)
P8 = Pregunta(8, "¿Que son los operadores logicos?", "Son operadores que comparan dos valores", "Son operadores que suman dos valores", "Son operadores que restan dos valores", 1)
P9 = Pregunta(9, "¿Que es un diccionario en programacion?", "Una lista de valores", "Una lista de claves y valores", "Una lista de funciones", 2)
P10 = Pregunta(10, "¿Para que sirve el operador %?", "Para sumar", "Para restar", "Para obtener el residuo de una division", 3)

Preguntas_Lista = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', Preguntas_Lista=Preguntas_Lista)

@app.route('/enviarquizz', methods=['POST'])
def Enviar():
    Respuestas_Correctas = 0
    resultados = []

    for pregunta in Preguntas_Lista:
        Pregunta_id = str(pregunta.p_id)
        opcion_elegida = request.form.get(Pregunta_id, "")
        respuesta_correcta = pregunta.Respuesta_Correcta()

        if opcion_elegida == respuesta_correcta:
            Respuestas_Correctas += 1
            resultados.append((pregunta.pregunta, opcion_elegida, "correcta"))
        else:
            resultados.append((pregunta.pregunta, opcion_elegida, "incorrecta"))

    return render_template('resultados.html', resultados=resultados, correctas=Respuestas_Correctas)

# Rutas de autenticación y contenido
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El usuario ya existe. Intenta con otro nombre de usuario.", "danger")
            return redirect("/register")
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session["user"] = username
            flash("Inicio de sesión exitoso.", "success")
            return redirect("/")
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
            return redirect("/login")
    
    return render_template("login.html")

@app.route('/')
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return redirect("/register")

@app.route('/index')
def index_redirect():
    return render_template('index.html')

@app.route("/logout")
def logout():
    session.pop("user", None)
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
