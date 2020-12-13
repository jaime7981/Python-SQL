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

### Funciones Aplicacion en Consola

#Tabula e imprime un querry en la consola devolviendo un True
def PrintQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        if len(request) == 0:
            print("No hay datos")
            return False
        description = []
        for desc in cur.description:
            description.append(desc[0])
        print(tabulate(request, headers = description, tablefmt="psql"))
        return True
    except:
        print("Querry ingresado no valido")
        return False

#Tabula un querry sin headers
def PrintQuerryNoHeaders(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        if len(request) == 0:
            print("No hay datos")
            return False
        print(tabulate(request, tablefmt="psql"))
        return True
    except:
        print("Querry ingresado no valido")
        return True

#Tabula un querry con los headers que uno le pase
def PrintQuerryCustomHeaders(text,headers):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        if len(request) == 0:
            print("No hay datos")
            return False
        print(tabulate(request,headers, tablefmt="psql"))
        return True
    except:
        print("Querry ingresado no válido")
        return False

#Muestra en la consola el listado de opciones (Para desarrollo de aplicacion en consola)
def DisplayMenu(lista_menu):
    counter = 1
    for titulo_opcion in lista_menu:
        print(str(counter) + ") " + str(titulo_opcion))
        counter += 1

#Funcion que valida que la opcion ingresada sea un numero del menu
def InputOpciones(menu):
    try:
        opcion = int(input())
        if opcion <= len(menu) and opcion > 0:
            return opcion
        else:
            print("No existe la opcion ingresada")
    except:
        print("Opcion no valida")

#Valida que el usuario y clave ingresada esten en la bbdd (Funciona para mi proyecto para la universidad pero es modificable para cualquier validacion)
def ValidacionUsuario(usuario, clave):
    usuarios_and_clave = SelectQuerry("SELECT email, contrasena FROM usuarios")
    for usuarios in usuarios_and_clave:
        if usuario == usuarios[0]:
            if clave == usuarios[1]:
                return True
    return False

#Sirve para verificar que el usuario metio un id que existe en la tabla (Para proyecto en consola)
def QuerryOptionIdCheck(querry, text):
    try:
        option = int(input(text))
        querry_check = SelectQuerry(querry)
        for check in querry_check:
            if check[0] == option:
                return option
        print("Opcion no valida")
        return 0
    except:
        print("Error de querry")
        return 0