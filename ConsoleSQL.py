import psycopg2 as svpg
from tabulate import tabulate
import PythonSQL as sql

class ColsoleSLQ(sql.SQLDatabase):
    def __init__(self, database, user, password, host, port):
        #sql.SQLDatabase.__init__(self, database, user, password, host, port)
        super().__init__(database, user, password, host, port)

    ### Funciones Aplicacion en Consola

    #Tabula e imprime un querry en la consola devolviendo un True
    def PrintQuerry(self, text):
        cur = self.con.cursor()
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
    def PrintQuerryNoHeaders(self, text):
        cur = self.con.cursor()
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
    def PrintQuerryCustomHeaders(self, text,headers):
        cur = self.con.cursor()
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
    def DisplayMenu(self, lista_menu):
        counter = 1
        for titulo_opcion in lista_menu:
            print(str(counter) + ") " + str(titulo_opcion))
            counter += 1

    #Funcion que valida que la opcion ingresada sea un numero del menu
    def InputOpciones(self ,menu):
        try:
            opcion = int(input())
            if opcion <= len(menu) and opcion > 0:
                return opcion
            else:
                print("No existe la opcion ingresada")
        except:
            print("Opcion no valida")

    #Valida que el usuario y clave ingresada esten en la bbdd (Funciona para mi proyecto para la universidad pero es modificable para cualquier validacion)
    def ValidacionUsuario(self, usuario, clave):

        usuarios_and_clave = self.SelectQuerry("SELECT email, contrasena FROM usuarios")
        for usuarios in usuarios_and_clave:
            if usuario == usuarios[0]:
                if clave == usuarios[1]:
                    return True
        return False

    #Sirve para verificar que el usuario metio un id que existe en la tabla (Para proyecto en consola)
    def QuerryOptionIdCheck(self, querry, text):
        try:
            option = int(input(text))
            querry_check = self.SelectQuerry(querry)
            for check in querry_check:
                if check[0] == option:
                    return option
            print("Opcion no valida")
            return 0
        except:
            print("Error de querry")
            return 0