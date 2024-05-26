import mysql.connector as mysql

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

