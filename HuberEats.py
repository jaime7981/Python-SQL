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

def InsertQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        return request
    except:
        print("Querry ingresado no valido")

def PrintQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        print(tabulate(request, tablefmt="psql"))
    except:
        print("Querry ingresado no valido")

def DisplayMenu(lista_menu):
    counter = 1
    for titulo_opcion in lista_menu:
        print(counter, ")", titulo_opcion)
        counter += 1

def ValidacionUsuario(usuario, clave):
    usuarios_and_clave = InsertQuerry("SELECT email, contrasena FROM usuarios")
    for usuarios in usuarios_and_clave:
        if usuario == usuarios[0]:
            if clave == usuarios[1]:
                return True
    return False

#quedan cosas por arreglar en esta funcion (podria ser opcional)
def InputOpciones():
    flag_opcion_correcta = True
    while flag_opcion_correcta:
        opcion = input()

    return opcion


#Programa principal
main = True

while main:
    login_menu = ["Ingrese querry",
                  "Iniciar Sesion", 
                  "Registrarse", 
                  "Exit"]
    DisplayMenu(login_menu)
    opcion = input()

    if opcion == "1":
        querry = input("Ingresar querry: ")
        PrintQuerry(querry)

    if opcion == "2":
        print("Iniciar Sesion\n")
        login_nombre_usuario = input("Ingresar nombre de usuario: ")
        login_clave = input("Ingresar clave: ")
        
        flag_menu_usuario = ValidacionUsuario(login_nombre_usuario, login_clave)

        if flag_menu_usuario == False:
            print("Usuario o clave incorrecta")

        while flag_menu_usuario:
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
            opcion = input()

            if opcion == "8":
                break
            if opcion == "9":
                main = False
                break

    if opcion == "3":
        while True:
            print("Bienvenido a Hubber Eats\nRegistrarse:\n")
            nombre_nuevo_usuario = input("Ingresar nombre de usuario: ")
            clave_nuevo_usuario = input("Ingresar clave: ")
            if len(clave_nuevo_usuario) <= 6:
                print("Clave no valida")
            if "@" not in nombre_nuevo_usuario or len(nombre_nuevo_usuario) > 4:
                print("Usuario no valido")
            if "@" in nombre_nuevo_usuario and len(clave_nuevo_usuario) > 6 and len(nombre_nuevo_usuario) > 4:
                print("usuario creado con exito")
                break

    if opcion == "4":
        main = False
    
    if opcion == "5":
        PrintQuerry("SELECT * FROM usuarios")

con.close()

