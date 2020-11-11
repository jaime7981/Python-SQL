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

menu_shoping_cart = []
product_shoping_cart = []

print("Conexion exitosa")
print("Bienveido")
#querry de ejemplo (locales, productos, pedidos, usuarios, menues, etc)
#SELECT * FROM categorias 
#con.commit()  // Actualiza los cambios en la base de datos, asi como los CREATE TABLE, UPDATES, INSERT, etc

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
        print(len(request))
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
        print("Exito al ejecutar DELETE querry")
    except:
        print("Error al intentar eliminar la linea")

#Muestra en la consola el listado de opciones
def DisplayMenu(lista_menu):
    counter = 1
    for titulo_opcion in lista_menu:
        print(str(counter) + ") " + str(titulo_opcion))
        counter += 1

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

#Valida que el usuario y clave ingresada esten en la bbdd 
def ValidacionUsuario(usuario, clave):
    usuarios_and_clave = SelectQuerry("SELECT email, contrasena FROM usuarios")
    for usuarios in usuarios_and_clave:
        if usuario == usuarios[0]:
            if clave == usuarios[1]:
                return True
    return False

#Sirve para verificar que el usuario metio un id que existe en la tabla
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

def ClearShopingCart():
    menu_shoping_cart.clear()
    product_shoping_cart.clear()

def AddToCart(product_menu_id, product_menu_flag):
    #True para producto False para menu
    try:
        if product_menu_flag == True:
            product_shoping_cart.append(product_menu_id)
        if product_menu_flag == False:
            menu_shoping_cart.append(product_menu_id)
    except:
        print("Parametros ingresados a AddToCart debe ser (int, bool)")

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
                while True:
                    PrintQuerry("SELECT * FROM locales")
                    opciones_locales = ["Seleccionar Local",
                                        "Agregar Local",
                                        "Volver Atras"]
                    DisplayMenu(opciones_locales)
                    opcion = InputOpciones(opciones_locales)
                    if opcion == 1:
                        id_local_seleccionado = QuerryOptionIdCheck("SELECT id_local FROM locales", 
                                                                    "Ingresar id local: ")
                        if id_local_seleccionado != 0:
                            while True:
                                PrintQuerry("SELECT * FROM locales WHERE id_local = " + str(id_local_seleccionado))
                                opcion_local_id = ["Editar Local",
                                                   "Eliminar Local",
                                                   "Ver Menus",
                                                   "Volver Atras"]
                                DisplayMenu(opcion_local_id)
                                opcion = InputOpciones(opcion_local_id)
                                if opcion == 1:
                                    print("Implementar editar local")

                                elif opcion == 2:
                                    delete_check = input("Seguro que desea eliminar este local (S/N) ")
                                    if delete_check == "S":
                                        DeleteQuerry("locales", "id_local = " + str(id_local_seleccionado))

                                elif opcion == 3:
                                    while True:
                                        PrintQuerry("SELECT * FROM menues WHERE id_local = " + str(id_local_seleccionado))
                                        opcion_menues = ["Seleccionar Menu",
                                                        "Agregar Menu",
                                                        "Volver Atras"]
                                        DisplayMenu(opcion_menues)
                                        opcion = InputOpciones(opcion_menues)
                                        if opcion == 1:
                                            id_menu_seleccionado = QuerryOptionIdCheck("SELECT id_menu FROM menues",
                                                                                        "Ingresar id menu: ")
                                            if id_menu_seleccionado != 0:
                                                while True:
                                                    large_querry = "SELECT pr.id_local, pr.id_producto, pr.nombre, pr.precio, pr.id_descuento \
                                                                FROM productos pr INNER JOIN \
                                                                (SELECT mp.id_producto FROM menu_producto mp INNER JOIN \
                                                                (SELECT men.id_menu FROM menues men WHERE id_menu = " + str(id_menu_seleccionado) + \
                                                                ") AS t1 ON mp.id_menu = t1.id_menu) AS t2 ON pr.id_producto = t2.id_producto"
                                                    PrintQuerry(large_querry)
                                                    opcion_menues = ["Agregar Menu Al Carrito",
                                                                        "Eliminar Producto Del Menu",
                                                                        "Editar Menu",
                                                                        "Eliminar Menu",
                                                                        "Descuento",
                                                                        "Volver Atras"]
                                                    DisplayMenu(opcion_menues)
                                                    opcion = InputOpciones(opcion_menues)
    
                                                    if opcion == 1:
                                                        AddToCart(id_menu_seleccionado, False)

                                                    elif opcion == 2:
                                                        id_producto_seleccionado = QuerryOptionIdCheck("SELECT mp.id_producto FROM menu_producto mp INNER JOIN \
                                                                            (SELECT men.id_menu FROM menues men WHERE id_menu = 20) AS t1 ON mp.id_menu = t1.id_menu",
                                                                            "Ingresar ID producto: ")
                                                        if id_producto_seleccionado != 0:
                                                            delete_product_from_menu = input("Eliminar el producto del menu? (S/N) ")
                                                            if delete_product_from_menu == "S":
                                                                DeleteQuerry("menu_producto", "id_menu = " + str(id_menu_seleccionado) + \
                                                                                                " AND id_producto = " + str(id_producto_seleccionado))
                                                        
                                                    elif opcion == 3:
                                                        print("Implementar editar menu")

                                                    elif opcion == 4:
                                                        print("Implementar eliminar menu")

                                                    elif opcion == 5:
                                                        print("Implementar opcion descuento")

                                                    elif opcion == 6:
                                                        break

                                        elif opcion == 2:
                                            print("implementar agregar menu")

                                        elif opcion == 3:
                                            break

                                elif opcion == 4:
                                    break

                    elif opcion == 2:
                        print("Agregar local")
                        nombre_local = "'" + input("Nombre local: ") + "'"
                        calle_local = "'" + input("Direccion local: ") + "'"
                        numero_local = input("Numero local: ")
                        comuna_local = "'" + input("Comuna local: ") + "'"
                        region_local = "'" + input("Region local: ") + "'"
                        aceptar_opcion = input("Esta seguro de esta informacion? (S/N) ")
                        if aceptar_opcion == "S":
                            InsertQuerry("locales", ("nombre", "calle", "numero", "comuna", "region"),
                                                    (nombre_local,
                                                     calle_local,
                                                     str(numero_local),
                                                     comuna_local,
                                                     region_local))

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

