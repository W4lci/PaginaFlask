from flask import Flask, render_template, request, session
from conectionBD import connect
import bd
import re

app = Flask(__name__, static_url_path="/static")
app.secret_key = bd.secret_key

conectando = connect(bd.bd_ip, bd.bd_usr, bd.bd_pwr, bd.bd_name)

BD = conectando if conectando != False else None
if BD == None:
    print("Error al conectar con la base de datos")

@app.route("/")
def hello_world():
    if session.get("usrid") == None:
        return render_template(
            "index.html",
            usr_conf="dropdown-item",
            usr_conf2="/registro", #a donde lleva el clic
            usr_conf3="Registrarse", #texto del boton
            usuario="Iniciar Sesión", 
            bs_conf="dropdown-item disabled")
    else: 
        return render_template(
            "index.html", 
            usr_conf="dropdown-item disabled",
            usr_conf2="/singout", #a donde lleva el clic
            usr_conf3="Cerrar Sesión", #texto del boton 
            usuario=session.get("usr"),
            bs_conf="dropdown-item"
        )
@app.route("/singout")
def singout():
    session.clear()
    return render_template(
        "index.html",
        usr_conf="dropdown-item",
        usr_conf2="/registro",
        usr_conf3="Registrarse",
        usuario="Iniciar Sesión", 
        bs_conf="dropdown-item disabled"
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = str(request.form["usuario"])
        password = str(request.form["password"])
        cursor = BD.cursor()
        if re.search("['\-#]", usuario) or re.search("['\-#]", password):
            return render_template("login.html", message="Caracteres no permitidos")
        cursor.execute(
            f"SELECT * FROM users WHERE usuario = '{usuario}' AND contrasenia = '{password}'"
        )
        result = cursor.fetchall()
        if len(result) > 0:
            session["usrid"] = result[0]
            session["usr"] = usuario
            return hello_world()
        else:
            return render_template(
                "login.html", message="Usuario o contraseña incorrectos"
            )
    else:
        return render_template("login.html", message="Error al enviar el formulario")


if __name__ == "__main__":
    app.run()
