from flask import Flask, render_template, request, session
from src.funciones import connect, login 
import src.credenciales as credenciales
import re

app = Flask(__name__, static_url_path="/static")
app.secret_key = credenciales.secret_key

conectando = connect(credenciales.bd_ip, credenciales.bd_usr, credenciales.bd_pwr, credenciales.bd_name)

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
def iniciar_sesion():
    message = '<div class="bg-dark text-white rounded-4 p-2">'
    if request.method == "POST":
        usuario = str(request.form["usuario"])
        password = str(request.form["password"])
        if re.search("['\-#]", usuario) or re.search("['\-#]", password):
            return render_template(
                "login.html",
                action="/login",
                tipo="Iniciar Sesión",
                boton="Iniciar Sesion",
                registrarse="Registrarse",
                olvidar="Olvidé mi contraseña",
                message=message + "Caracteres no permitidos</div>",
            )

        result = login(usuario, password)
        if result:
            session["usrid"] = result[0][0]
            session["usr"] = usuario
            return hello_world()
        elif result == "Db error":
            return render_template(
                "login.html",
                message=message + "Error en la base de datos</div>",
            )
        else: 
            return render_template(
                "login.html",
                message=message + "Usuario o contraseña incorrectos</div>",
            )

    else:
        return render_template(
            "login.html",
            message="<div></div>",
        )


if __name__ == "__main__":
    app.run()
