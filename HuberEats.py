import psycopg2 as svpg
from tabulate import tabulate
import os
cls = lambda: os.system('cls') #sirve para limiar la consola (Para cuando lo tengamos listo)

con = svpg.connect(database="grupo6", 
                 user="grupo6", 
                 password="99sFKQ", 
                 host="201.238.213.114", 
                 port="54321")

print("Conexion exitosa")

#SELECT * FROM categorias  // querry de ejemplo (locales, productos, pedidos, usuarios, menues, etc)
#con.commit()  // Actualiza los cambios en la base de datos, 
#                   asi como los CREATE TABLE o UPDATES, etc


def InsertQuerry(text):
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

def InputOpciones(): #quedan cosas por arreglar (va a servir para controlar el input de la consola si es que usamos case: para el menu)
    flag_opcion_correcta = True
    while flag_opcion_correcta:
        opcion = input()

    return opcion

main = True

while main:
    login_menu = ["Ingrese querry","Iniciar Sesion", "Registrarse", "Exit"]
    DisplayMenu(login_menu)
    opcion = input()

    if opcion == "1":
        querry = input("Ingresar querry: ")
        InsertQuerry(querry)

    if opcion == "2":
        print("Iniciar Sesion\n")
        login_nombre_usuario = input("Ingresar nombre de usuario: ")
        login_clave = input("Ingresar clave: ")
        while True:
            menu_entrada_usuario = ["Locales", "Categorias", "Promociones", "Direcciones", "Carrito", "Historial de pedidos", "Repartidores", "Cerrar Sesion", "Exit"]
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
            if len(clave_nuevo_usuario) > 6 and len(nombre_nuevo_usuario) > 4:
                print("usuario creado")
                break

    if opcion == "4":
        main = False
    
    if opcion == "5":
        InsertQuerry("SELECT * FROM usuarios") #opcion secreta para mostrar a los usuarios

con.close()

