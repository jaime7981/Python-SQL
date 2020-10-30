import psycopg2 as svpg
from tabulate import tabulate
import os

#sirve para limpiar la consola (Para cuando lo tengamos listo)
cls = lambda: os.system('cls')

con = svpg.connect(database="grupo6", 
                 user="grupo6", 
                 password="99sFKQ", 
                 host="201.238.213.114", 
                 port="54321")

print("Conexion exitosa")

#querry de ejemplo (locales, productos, pedidos, usuarios, menues, etc)
#SELECT * FROM categorias 
#con.commit()  // Actualiza los cambios en la base de datos, 
#                   asi como los CREATE TABLE, UPDATES, INSERT, etc

#Devuelve un querry
def InsertQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        return request
    except:
        print("Querry ingresado no valido")

#Tabula e imprime un querry en la consola
def PrintQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        print(tabulate(request, tablefmt="psql"))
    except:
        print("Querry ingresado no valido")

#Muestra en la consola el listado de opciones
def DisplayMenu(lista_menu):
    counter = 1
    for titulo_opcion in lista_menu:
        print(counter, ")", titulo_opcion)
        counter += 1

#Valida que el usuario y clave ingresada esten en la bbdd 
def ValidacionUsuario(usuario, clave):
    usuarios_and_clave = InsertQuerry("SELECT email, contrasena FROM usuarios")
    for usuarios in usuarios_and_clave:
        if usuario == usuarios[0]:
            if clave == usuarios[1]:
                return True
    return False

#Funcion que valida que la opcion ingresada sea un numero
def InputOpciones(menu):
    try:
        opcion = int(input())
        if opcion <= len(menu) and opcion > 0:
            return opcion
        else:
            print("No existe la opcion ingresada")
    except:
        print("Opcion no valida")


#Programa principal
main = True

while main:
    #Menu de inicio
    login_menu = ["Ingrese querry",
                  "Iniciar Sesion", 
                  "Registrarse", 
                  "Exit"]
    DisplayMenu(login_menu)
    opcion = InputOpciones(login_menu)

    if opcion == 1:
        querry = input("Ingresar querry: ")
        PrintQuerry(querry)

    if opcion == 2:
        #Validacion login
        print("Iniciar Sesion\n")
        login_nombre_usuario = input("Ingresar nombre de usuario: ")
        login_clave = input("Ingresar clave: ")
        flag_menu_usuario = ValidacionUsuario(login_nombre_usuario, login_clave)
        if flag_menu_usuario == False:
            print("Usuario o clave incorrecta")

        while flag_menu_usuario:
            #Menu principal
            menu_entrada_usuario = ["Locales", 
                                    "Categorias", 
                                    "Promociones", 
                                    "Direcciones", 
                                    "Carrito", 
                                    "Historial de pedidos", 
                                    "Repartidores", 
                                    "Cerrar Sesion", 
                                    "Exit"]
            DisplayMenu(menu_entrada_usuario)
            opcion = InputOpciones(menu_entrada_usuario)

            if opcion == 8:
                break

            if opcion == 9:
                main = False
                break

    if opcion == 3:
        while True:
            print("Bienvenido a Hubber Eats\nRegistrarse:\n")
            nombre_nuevo_usuario = input("Ingresar nombre de usuario: ")
            clave_nuevo_usuario = input("Ingresar clave: ")

            if len(clave_nuevo_usuario) <= 6:
                print("Clave no valida")

            if "@" in nombre_nuevo_usuario and (".com" in nombre_nuevo_usuario or ".cl" in nombre_nuevo_usuario)\
                and len(clave_nuevo_usuario) > 6 and len(nombre_nuevo_usuario) > 8:
                print("usuario creado con exito")
                break
            else:
                print("Usuario no valido")

    if opcion == 4:
        main = False
    
    if opcion == 5:
        PrintQuerry("SELECT * FROM usuarios")

con.close()

