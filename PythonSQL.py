import psycopg2 as svpg
from tabulate import tabulate

#Se conecta a la bbdd
try:
    con = svpg.connect(database="grupo6",
                       user="grupo6",
                       password="99sFKQ",
                       host="201.238.213.114",
                       port="54321")
    print("Conexion exitosa")
except:
    print("No se pudo conectar a la bbdd")

## Funciones PostgreSQL

#Devuelve una matriz del querry introducido
def SelectQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        if len(request) == 0:
            return False
        return request
    except:
        print("Querry ingresado no valido")
        return False

#InsertQuerry("nombre tabla", ("col1", "col2", "col3"), ("dato1", "dato2", "dato3"))
def InsertQuerry(table, columns, parameters):

    parameters_string = ""
    for a in range(len(parameters)):
        try:
            try:
                parameters_string += "(" + int(parameters(a)) + ")"
            except:
                parameters_string += "(" + float(parameters(a)) + ")"
        except:
            parameters_string += "('" + parameters(a) + "')"
        if a < len(parameters):
            parameters_string += ","

    columns_string = "(" + ", ".join(columns) + ")"

    if len(parameters) > 0:
        cur = con.cursor()
        if len(columns_string) == 2:
            try:
                insertstr = "INSERT INTO {} VALUES {}".format(table, parameters_string)
                cur.execute(insertstr)
                con.commit()
                return True
            except:
                print("Querry ingresado no valido")
                return False
        elif len(columns_string) > 2:
            try:
                insertstr = "INSERT INTO {} {} VALUES {}".format(table, columns_string, parameters_string)
                cur.execute(insertstr)
                con.commit()
                return True
            except:
                print("Querry ingresado no valido")
                return False
    else:
        print("Insert no tiene valores")
        return False

#Elimina una linea de la bbdd DeleteQuerry("table name", "logic operation")
def DeleteQuerry(table, where):
    cur = con.cursor()
    try:
        querry_text = "DELETE FROM {} WHERE {}".format(table,where)
        cur.execute(querry_text)
        con.commit()
        print("Exito al ejecutar DELETE querry")
        return True
    except:
        print("Error al intentar eliminar la linea")
        return False

#Modifica una linea de la bbdd DeleteQuerry("table name", "paremeter = new_parameter", "logic operation")
def UpdateQuerry(table, columns, parameters, where):
    cur = con.cursor()
    update_sql = ""
    for a in range(len(columns)):
        try:
            try:
                update_sql += "{} = {}".format(columns[a], int(parameters[a]))
            except:
                update_sql += "{} = {}".format(columns[a], float(parameters[a]))
        except:
            update_sql += "{} = '{}'".format(columns[a], parameters[a])

    try:
        querry_text = "UPDATE {} SET {} WHERE {}".format(table, update_sql, where)
        cur.execute(querry_text)
        con.commit()
        print("Exito al ejecutar UPDATE querry")
        return True
    except:
        print("Error al intentar modificar la linea")
        return False

#Cierra la conexion a la bbdd
def CloseSV():
    con.close()

#Pasa la informacion de la conexion a la bbdd
def GetCon():
    return con
