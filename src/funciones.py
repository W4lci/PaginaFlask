import mysql.connector as mysql
import src.credenciales as cr
def connect(ip, user, password, database):
    bd = None
    try:
        bd = mysql.connect(
            host=ip,
            user=user,
            password=password,
            database=database
        )
    except Exception as e:
        print(e)
        return False
    return bd

def login(usuario, password):
    result = None
    try:
        bd = connect(cr.bd_ip, cr.bd_usr, cr.bd_pwr, cr.bd_name)
        cursor = bd.cursor()
        cursor.execute(
            f"SELECT * FROM users WHERE usuario = '{usuario}' AND contrasenia = '{password}'"
        )
        result = cursor.fetchall()
        bd.close()
        if len(result) > 0:  
            return result
        else:
            return False
    except Exception as e:
        print(e)
        return "Db error"


def register(usuario, password):
    try:
        bd = connect(cr.bd_ip, cr.bd_usr, cr.bd_pwr, cr.bd_name)
        cursor = bd.cursor()
        cursor.execute(
            f"INSERT INTO users (usuario, contrasenia) VALUES ('{usuario}', '{password}')"
        )
        bd.commit()
        bd.close()
        return True
    except Exception as e:
        print(e)
        return False