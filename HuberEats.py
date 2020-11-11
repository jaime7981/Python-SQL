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


###FUNCIONES LORENZINI ----
def PrintQuerryJ(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        print(tabulate(request, tablefmt="psql"))
    except:
        print("Querry ingresado no valido")

def PrintQuerry2(text,headers):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        return tabulate(request,headers, tablefmt="psql")
    except:
        print("Querry ingresado no válido")

def QuerryOptionIdCheck2(querry, option):
    try:
        option=option
        querry_check = SelectQuerry(querry)
        for check in querry_check:
            if check[0] == option:
                return option
        print("Opcion no valida")
        return 0
    except:
        print("Error de querry")
        return 0

#Historial de pedido
def Historial_pedidos(login_nombre_usuario):
    id_user= SelectQuerry(f"SELECT id_usuario FROM Usuarios WHERE email='{login_nombre_usuario}'")
    id_user= id_user[0][0] #ID del usuario
    
    menu=True
    while menu:
        print("\nHistorial de pedidos\n")
        
        headers=["ID","Dirección","# ", "Fecha","Monto"]
        sql= PrintQuerry2(f"SELECT id_pedido, calle,numero, fecha_pedido, monto FROM (SELECT id_pedido, (monto_producto+COALESCE(monto_menu,0)) AS monto FROM (SELECT id_pedido, monto_producto, monto_menu FROM (SELECT DISTINCT  id_pedido,  (cantidad_producto*precio) AS monto_producto \
        FROM pedido_producto INNER JOIN productos \
        USING(id_producto) \
        ORDER BY id_pedido) AS t1 FULL JOIN (SELECT DISTINCT  id_pedido,  SUM((cantidad_menu*precio)) AS monto_menu \
        FROM pedido_menu INNER JOIN menues \
        USING(id_menu) \
        GROUP BY id_pedido \
        ORDER BY id_pedido) AS t2 \
        USING(id_pedido)) AS t5) AS t3 INNER JOIN (SELECT id_pedido, id_usuario, calle , numero, fecha_pedido \
        FROM Pedidos INNER JOIN Direcciones \
        USING(id_direccion)) AS t4 \
        USING(id_pedido) \
        WHERE id_usuario={id_user}",headers)
        print(sql) #Pedidos de Usuario
        
        menu_historial=["Ver pedido",
                        "Volver a Menú"] #Menu_Historial_de_pedidos
        DisplayMenu(menu_historial)
        option_historial = InputOpciones(menu_historial)
        
        if option_historial==1:
            whatch_order=True
            while whatch_order:
                print("Ver pedido\n")
                print(sql)
                text="Ingrese el pedido que desea ver:"
                querry=f"SELECT id_pedido FROM Pedidos WHERE id_usuario={id_user}"
                id_order= QuerryOptionIdCheck(querry,text)
                if id_order!=0:
                    headers=["ID","Dirección","# ", "Fecha","Monto"]
                    sql_2= PrintQuerry2(f"SELECT id_pedido, calle,numero, fecha_pedido, monto FROM (SELECT id_pedido, (monto_producto+COALESCE(monto_menu,0)) AS monto FROM (SELECT id_pedido, monto_producto, monto_menu FROM (SELECT DISTINCT  id_pedido,  (cantidad_producto*precio) AS monto_producto \
                                        FROM pedido_producto INNER JOIN productos \
                                        USING(id_producto) \
                                        ORDER BY id_pedido) AS t1 FULL JOIN (SELECT DISTINCT  id_pedido,  SUM((cantidad_menu*precio)) AS monto_menu \
                                        FROM pedido_menu INNER JOIN menues \
                                        USING(id_menu) \
                                        GROUP BY id_pedido \
                                        ORDER BY id_pedido) AS t2 \
                                        USING(id_pedido)) AS t5) AS t3 INNER JOIN (SELECT id_pedido, id_usuario, calle , numero, fecha_pedido \
                                        FROM Pedidos INNER JOIN Direcciones \
                                        USING(id_direccion)) AS t4 \
                                        USING(id_pedido) \
                                        WHERE id_usuario={id_user} AND id_pedido={id_order}",headers)
                    print(sql_2)#Informacion solo del pedido que se seleccionó
                    
                    id_check= id_order
                    querry_product= f"SELECT id_pedido FROM Pedido_producto WHERE id_pedido={id_order}"
                    querry_menu=f"SELECT id_pedido FROM Pedido_menu WHERE id_pedido={id_order}"
                    id_checkproduct= QuerryOptionIdCheck2(querry_product,id_check)
                    id_checkmenu= QuerryOptionIdCheck2(querry_menu,id_check)
                    
                    if id_checkproduct!=0 and id_checkmenu!=0:
                        headers_detail=["ID","Nombre", "Cantidad","Precio unitario","Descuento"]
                        
                        #Detalle del producto
                        sql_product_detail= PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                                        FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                                        USING(id_producto)\
                                                        WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                                        WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                                        WHERE id_usuario= {id_user}",headers_detail)
    
                        #Detalle del menu
                        sql_menu_detail= PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                                      FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                                      FROM pedido_menu INNER JOIN Menues \
                                                      USING(id_menu)\
                                                      WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                                      WHERE id_usuario={id_user}",headers_detail)
                                                      
                        #Detalle del pedido
                        print("\nDetalle del pedido")
                        print("\nProductos")
                        print(sql_product_detail)
                        print("\nMenues")
                        print(sql_menu_detail)
                        
                        #Promoción aplicada
                        sql_promo= SelectQuerry(f"SELECT DISTINCT id_usuario, id_pedido,COALESCE(nombre,'NO APLICA'), COALESCE(monto,0) FROM Pedidos \
                                                FULL JOIN (SELECT id_codigo, nombre, monto FROM Promocion_usuario INNER JOIN Promociones USING(id_codigo)) AS t1\
                                                USING(id_codigo)\
                                                WHERE id_usuario={id_user} AND id_pedido={id_order}")
                        #monto y nombre de la promoción
                        monto_promo= sql_promo[0][3]
                        nombre_promo= sql_promo[0][2]
                        
                        if monto_promo!=0:
                            #Hay promoción aplicada
                            print("\nPromoción -->",nombre_promo,"$"+str(monto_promo))
                        else:
                            #No hay promocion aplicada
                            print("\nPromoción -->",nombre_promo)
                        
                        #Valor final del pedido
                        #Solo los productos
                        tp=0
                        data1= SelectQuerry(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                            USING(id_producto)\
                                            WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                            WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                            WHERE id_usuario= {id_user}")
                        data2= SelectQuerry(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                            FROM pedido_menu INNER JOIN Menues \
                                            USING(id_menu)\
                                            WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                            WHERE id_usuario={id_user}")
                        for a in range(len(data1)):
                            quantity_product= data1[a][2]
                            price_product= data1[a][3]
                            discount_product= data1[a][4]
                            #Total precio por la cantidad de productos pedidos
                            total_pricep= price_product*quantity_product 
                            if 0<discount_product<100: 
                                #Descuento por %
                                total_pricep_discount= total_pricep-(total_pricep*discount_product)/100
                                tp+=total_pricep_discount
                            if discount_product>100:
                                #Descuento por valor
                                total_pricep_discount= total_pricep-(quantity_product*discount_product)
                                tp+=total_pricep_discount
                            if discount_product==0:
                                #No tenga descuento
                                total_pricep_discount=total_pricep
                                tp+=total_pricep_discount
                                
                        #Solo los menues
                        tm=0
                        for b in range(len(data2)):
                            quantity_menu= data2[b][2]
                            price_menu= data2[b][3]
                            discount_menu= data2[b][4]
                            #Total precio por la cantidad de menues pedidos
                            total_pricem= price_menu*quantity_menu
                            if 0<discount_menu<100: 
                                #Descuento por %
                                total_pricem_discount= total_pricem-(total_pricem*discount_menu)/100
                                tm+=total_pricem_discount
                            if discount_menu>100:
                                #Descuento por valor
                                total_pricem_discount= total_pricem-(quantity_menu*discount_menu)
                                tm+=total_pricem_discount
                            if discount_menu==0:
                                #No tenga descuento
                                total_pricem_discount=total_pricem
                                tm+=total_pricem_discount
                        
                        #Operacion para valor final 
                        total= int(tp+tm)-monto_promo
                        print("Valor final del pedido -->","$"+str(total))
                        pass
                    
                    if id_checkproduct!=0 and id_checkmenu==0:
                        headers_detail=["ID","Nombre", "Cantidad","Precio unitario","Descuento"]
                        
                        #Detalle del producto
                        sql_product_detail= PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                                        FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                                        USING(id_producto)\
                                                        WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                                        WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                                        WHERE id_usuario= {id_user}",headers_detail)
                                                
                        #Detalle del pedido
                        print("\nDetalle del pedido")
                        print("\nProductos")
                        print(sql_product_detail)
                        
                        #Promoción aplicada
                        sql_promo= SelectQuerry(f"SELECT DISTINCT id_usuario, id_pedido,COALESCE(nombre,'NO APLICA'), COALESCE(monto,0) FROM Pedidos \
                                                FULL JOIN (SELECT id_codigo, nombre, monto FROM Promocion_usuario INNER JOIN Promociones USING(id_codigo)) AS t1\
                                                USING(id_codigo)\
                                                WHERE id_usuario={id_user} AND id_pedido={id_order}")
                        #monto y nombre de la promoción
                        monto_promo= sql_promo[0][3]
                        nombre_promo= sql_promo[0][2]
                        
                        if monto_promo!=0:
                            #Hay promoción aplicada
                            print("\nPromoción -->",nombre_promo,"$"+str(monto_promo))
                        else:
                            #No hay promocion aplicada
                            print("\nPromoción -->",nombre_promo)
                        
                        #Valor final del pedido
                        #Solo los productos
                        tp=0
                        data1= SelectQuerry(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                            USING(id_producto)\
                                            WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                            WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                            WHERE id_usuario= {id_user}")
                        for a in range(len(data1)):
                            quantity_product= data1[a][2]
                            price_product= data1[a][3]
                            discount_product= data1[a][4]
                            #Total precio por la cantidad de productos pedidos
                            total_pricep= price_product*quantity_product 
                            if 0<discount_product<100: 
                                #Descuento por %
                                total_pricep_discount= total_pricep-(total_pricep*discount_product)/100
                                tp+=total_pricep_discount
                            if discount_product>100:
                                #Descuento por valor
                                total_pricep_discount= total_pricep-(quantity_product*discount_product)
                                tp+=total_pricep_discount
                            if discount_product==0:
                                #No tenga descuento
                                total_pricep_discount=total_pricep
                                tp+=total_pricep_discount
                                
                        #Operacion para valor final 
                        total= int(tp)-monto_promo
                        print("Valor final del pedido -->","$"+str(total))
                        pass
                    
                    if id_checkproduct==0 and id_checkmenu!=0:
                        headers_detail=["ID","Nombre", "Cantidad","Precio unitario","Descuento"]
                        
                        #Detalle del menu
                        sql_menu_detail= PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                                      FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                                      FROM pedido_menu INNER JOIN Menues \
                                                      USING(id_menu)\
                                                      WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                                      WHERE id_usuario={id_user}",headers_detail)
                        
                        #Detalle del pedido
                        print("\nDetalle del pedido")
                        print("\nMenues")
                        print(sql_menu_detail)
                        
                        #Promoción aplicada
                        sql_promo= SelectQuerry(f"SELECT DISTINCT id_usuario, id_pedido,COALESCE(nombre,'NO APLICA'), COALESCE(monto,0) FROM Pedidos \
                                                FULL JOIN (SELECT id_codigo, nombre, monto FROM Promocion_usuario INNER JOIN Promociones USING(id_codigo)) AS t1\
                                                USING(id_codigo)\
                                                WHERE id_usuario={id_user} AND id_pedido={id_order}")
                        #monto y nombre de la promoción
                        monto_promo= sql_promo[0][3]
                        nombre_promo= sql_promo[0][2]
                        
                        if monto_promo!=0:
                            #Hay promoción aplicada
                            print("\nPromoción -->",nombre_promo,"$"+str(monto_promo))
                        else:
                            #No hay promocion aplicada
                            print("\nPromoción -->",nombre_promo)
                        
                        data2= SelectQuerry(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                            FROM pedido_menu INNER JOIN Menues \
                                            USING(id_menu)\
                                            WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                            WHERE id_usuario={id_user}")
                        tm=0
                        for b in range(len(data2)):
                            quantity_menu= data2[b][2]
                            price_menu= data2[b][3]
                            discount_menu= data2[b][4]
                            #Total precio por la cantidad de menues pedidos
                            total_pricem= price_menu*quantity_menu
                            if 0<discount_menu<100: 
                                #Descuento por %
                                total_pricem_discount= total_pricem-(total_pricem*discount_menu)/100
                                tm+=total_pricem_discount
                            if discount_menu>100:
                                #Descuento por valor
                                total_pricem_discount= total_pricem-(quantity_menu*discount_menu)
                                tm+=total_pricem_discount
                            if discount_menu==0:
                                #No tenga descuento
                                total_pricem_discount=total_pricem
                                tm+=total_pricem_discount
                        
                        #Operacion para valor final 
                        total= int(tm)-monto_promo
                        print("Valor final del pedido -->","$"+str(total))
                        pass
                        
                    else:
                        whatch_order=False
                        continue
                else:
                    continue
                break
            ##
            flag=True
            while flag:
                headers=["Pedido","Repartidor","Nombre","Teléfono","Vehículo","Patente"]
                sql_repartidor= PrintQuerry2(f"SELECT id_pedido,id_repartidor, nombre, telefono, vehiculo, patente \
                                 FROM Pedidos INNER JOIN Repartidores \
                                 USING(id_repartidor)\
                                 WHERE id_pedido={id_order}",headers)
                nombre_repartidor= SelectQuerry(f"SELECT nombre \
                                                FROM Pedidos INNER JOIN Repartidores \
                                                USING(id_repartidor)\
                                                WHERE id_pedido={id_order}")
                nombre_repartidor= nombre_repartidor[0][0]
                print("\nInformacion del repartidor")
                print(sql_repartidor)
                menu_dar_rating=["Dar rating",
                                 "Volver a Historial de Pedidos"]
                DisplayMenu(menu_dar_rating)
                option = InputOpciones(menu_dar_rating)
                if option==1:
                    print(f"\nDar rating a {nombre_repartidor} ")
                    print(sql_repartidor)
                    menu_puntuacion=["★",
                                     "★★",
                                     "★★★",
                                     "★★★★",
                                     "★★★★★",
                                     "Volver a Ver Pedido"]
                    DisplayMenu(menu_puntuacion)
                    option_rating = InputOpciones(menu_puntuacion)
                    
                    if option_rating==1 or option_rating==2 or option_rating==3 or option_rating==4 or option_rating==5:
                        sql_puntuacion= SelectQuerry(f"SELECT puntuacion_repartidor \
                                                     FROM Pedidos INNER JOIN Repartidores \
                                                     USING(id_repartidor)\
                                                     WHERE id_pedido={id_order} AND puntuacion_repartidor IS null")
                        if sql_puntuacion!=[]:
                            sql_update= PrintQuerryJ(f"UPDATE Pedidos SET puntuacion={option_rating} \
                                                    WHERE id_pedido={id_order} AND puntuacion_repartidor IS NULL")
                        else:
                            print("El repartidor ya ha recibido una puntuación por parte de este usuario")
                            break
                    else:
                        continue
                    break
                
                if option==2:
                    flag=False
                    pass
                    
                else:
                    continue
                
        if option_historial==2:
            menu=False
            pass 
        
def Repartidores():
    menu=True
    while menu:
        print("\nRepartidores")
        headers= ["ID","Nombre","Patente"]
        sql= PrintQuerry2("SELECT id_repartidor, nombre, patente \
                          FROM Repartidores \
                          ORDER BY id_repartidor",headers)
        print(sql)
        menu_repartidor=["Ver Repartidor",
                         "Agregar repartidor",
                         "Volver al Menú Principal"]
        DisplayMenu(menu_repartidor)
        option=InputOpciones(menu_repartidor)
        if option==1:
            text="Ingrese el ID del repartidor que desea ver:"
            querry="SELECT*FROM Repartidores"
            option_repartidor= QuerryOptionIdCheck(querry, text)
            flag_repartidor=True
            while flag_repartidor:
                if option_repartidor!=0:
                    headers=["ID","Nombre","teléfono","vehículo","patente"]
                    sql=PrintQuerry2(f"SELECT*FROM Repartidores WHERE id_repartidor={option_repartidor}",headers)
                    print(sql)
                    menu_ver_repartidor=["Editar Repartidor",
                                         "Eliminar repartidor",
                                         "Volver a Opciones repartidor"]
                    DisplayMenu(menu_ver_repartidor)
                    option_ver_repartidor=InputOpciones(menu_repartidor)
                    flag_editor=True
                    while flag_editor: 
                        if option_ver_repartidor==1:
                            print("\nEditar a repartidor")
                            print("\nSeleccione el campo que desea editar")
                            menu_editor=["Nombre",
                                         "Teléfono",
                                         "Vehículo y patente",
                                         "Editar todo",
                                         "Volver a Editar repartidor"]
                            DisplayMenu(menu_editor)
                            option_editor=InputOpciones(menu_editor)
                            if option_editor==1:
                                new_name=input("Ingrese el nuevo nombre del repartidor:")
                                slq_update1= PrintQuerryJ(f"UPDATE Repartidores SET nombre='{new_name}' WHERE id_repartidor={option_repartidor}")
                                print("El repartidor ha sido editado exitosamente")
                                pass
                            if option_editor==2:
                                new_number=int(input("Ingrese el nuevo numero del repartidor:"))
                                slq_update2= PrintQuerryJ(f"UPDATE Repartidores SET telefono={new_number} WHERE id_repartidor={option_repartidor}")
                                print("El telefono del repartidor ha sido editado exitosamente")
                                pass
                            if option_editor==3:
                                new_vehicle=input("Ingrese el nuevo vehículo del repartidor:")
                                new_patent=input("Ingrese la patente del vehículo. En el caso de ser una bicicleta precione ENTER")
                                slq_update3= PrintQuerryJ(f"UPDATE Repartidores SET vehículo='{new_vehicle}, patente='{new_patent}' WHERE id_repartidor={option_repartidor}")
                                print("El vehículo y la patente han sido editados exitosamente")
                                pass
                            if option_editor==4:
                                new_name=input("Ingrese el nuevo nombre del repartidor:")
                                new_number=int(input("Ingrese el nuevo numero del repartidor:"))
                                new_vehicle=input("Ingrese el nuevo vehículo del repartidor:")
                                new_patent=input("Ingrese la patente del vehículo. En el caso de ser una bicicleta precione ENTER")
                                sql_update4= PrintQuerryJ(f"UPDATE Repartidores SET nombre='{new_name}',telefono={new_number},vehiculo='{new_vehicle}', patente='{new_patent}' WHERE id_repartidor={option_repartidor}")
                                print("Los campos del repartidor han sido editados exitosamente")
                                pass
                            if option_editor==5:
                                flag_editor=False
                                break
        
                        if option_ver_repartidor==2:
                            print("\n¿Estas seguro que deseas eliminar a este repartidor?" )
                            yes_no= ["Sí, estoy seguro",
                                     "No estoy seguro"]
                            DisplayMenu(yes_no)
                            option_delete=InputOpciones(yes_no)
                            if option_delete==1:
                                querry=f"DELETE FROM Repartidores WHERE id_repartidor={option_repartidor}" 
                                sql_delete= PrintQuerryJ(querry)
                                print("El repartidor se ha eliminado exitosamente")
                                break
                            if option_delete==2:
                                flag_editor=False
                                break
                                
    
                        if option_ver_repartidor==3:
                            flag_repartidor=False
                            break
                if option_repartidor==0:
                    flag_repartidor=False
                    break
                break
            
        if option==2:
            print("\nAgregar repartidor")
            table="Repartidores"
            new_name=input("Ingrese el nombre:")
            new_number=int(input("Ingrese el telefono:"))
            new_vehicle= input("Ingrese el tipo de vehículo (moto, motobico, bici):")
            new_patent=input("Ingrese la patente del vehículo; Si no tiene patente presione ENTER:")
            cur = con.cursor()
            insertstr = f"INSERT INTO {table}(nombre,telefono,vehiculo,patente) values('{new_name}',{new_number},'{new_vehicle}','{new_patent}')"
            cur.execute(insertstr)
            con.commit()
            print("\nRepartidor añadido con exito")
            
        if option==3:
            menu=False
            break        
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
                Historial_pedidos(login_nombre_usuario)
                pass

            elif opcion == 7:
                Repartidores()
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

