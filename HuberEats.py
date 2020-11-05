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
def SelectQuerry(text):
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
        description = []
        for desc in cur.description:
            description.append(desc[0])
        print(tabulate(request, headers = description, tablefmt="psql"))
    except:
        print("Querry ingresado no valido")

#InsertTest("nombre tabla", ("col1", "col2", "col3"), ("dato1", "dato2", "dato3"))
#
def InsertQuerry(table, lista_columnas, lista_datos):

    lista_d = "(" + ", ".join(lista_datos) + ")"
    lista_c = "(" + ", ".join(lista_columnas) + ")"

    if len(lista_datos) > 0:
        cur = con.cursor()
        if len(lista_c) == 2:
            try:
                insertstr = "INSERT INTO " + table + " VALUES " + lista_d
                cur.execute(insertstr)
                con.commit()
                return True
            except:
                print("Querry ingresado no valido")
                return False
        elif len(lista_c) > 2:
            try:
                insertstr = "INSERT INTO " + table + lista_c + " VALUES " + lista_d
                cur.execute(insertstr)
                con.commit()
                return True
            except:
                print("Querry ingresado no valido")
                return False
    else:
        print("Insert no tiene valores")
        return False

#Elimina una linea
def DeleteQuerry(table, text):
    cur = con.cursor()
    try:
        querry_text = "DELETE FROM " + table + " WHERE " + text
        cur.execute(querry_text)
        con.commit()
    except:
        print("Error al intentar eliminar la linea")

#Muestra en la consola el listado de opciones
def DisplayMenu(lista_menu):
    counter = 1
    for titulo_opcion in lista_menu:
        print(str(counter) + ") " + str(titulo_opcion))
        counter += 1

#Valida que el usuario y clave ingresada esten en la bbdd 
def ValidacionUsuario(usuario, clave):
    usuarios_and_clave = SelectQuerry("SELECT email, contrasena FROM usuarios")
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
                  "Exit",
                  "Ver Usuarios"]
    DisplayMenu(login_menu)
    opcion = InputOpciones(login_menu)

    if opcion == 1:
        querry = input("Ingresar querry: ")
        PrintQuerry(querry)

    elif opcion == 2:
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

            if opcion == 1:
                PrintQuerry("SELECT * FROM locales OREDER BY id_local DES")
                while True:
                    opciones_locales = ["Ver Local",
                                        "Agregar Local",
                                        "Volver Atras"]
                    DisplayMenu(opciones_locales)
                    opcion = InputOpciones(opciones_locales)
                    if opcion == 1:
                        id_local = input("Ingresar numero de local para ver opciones")
                    elif opcion == 2:
                        print("Agregar local")
                    elif opcion == 3:
                        break

            elif opcion == 2:
                pass

            elif opcion == 3:
                pass

            elif opcion == 4:
                pass

            elif opcion == 5:
                pass

            elif opcion == 6:
                pass

            elif opcion == 7:
                pass

            elif opcion == 8:
                break

            elif opcion == 9:
                main = False
                break

    elif opcion == 3:
        while True:
            print("Bienvenido a Hubber Eats\nRegistrarse:\n")
            nombre_apellido = "'" + input("Ingresar nombre y apellido: ") + "'"
            nombre_usuario = "'" + input("Ingresar usuario: ") + "'"
            clave_nuevo_usuario = "'" + input("Ingresar clave: ") + "'"
            numero_usuario = input("Ingresar numero de telefono: ")

            if len(clave_nuevo_usuario) <= 6:
                print("Clave no valida")

            if "@" in nombre_usuario \
                and (".com" in nombre_usuario or ".cl" in nombre_usuario)\
                and len(clave_nuevo_usuario) > 6 and len(nombre_usuario) > 8\
                and len(numero_usuario) == 9:
                nuevo_id_usuario = SelectQuerry("SELECT id_usuario FROM usuarios")

                crear_usuario = InsertQuerry("usuarios", (), (str(len(nuevo_id_usuario) + 1),
                                                                nombre_apellido, 
                                                                nombre_usuario, 
                                                                clave_nuevo_usuario, 
                                                                numero_usuario))

                if crear_usuario == True:
                    print("usuario creado con exito")
                    break
                else:
                    print("Error al crear usuario")
                    break

            else:
                print("Usuario no valido")

    elif opcion == 4:
        main = False
    
    elif opcion == 5:
        PrintQuerry("SELECT * FROM usuarios")

con.close()

