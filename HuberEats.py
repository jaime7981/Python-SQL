import psycopg2 as svpg
import tabulate

con = svpg.connect(database="grupo6", 
                 user="grupo6", 
                 password="99sFKQ", 
                 host="201.238.213.114", 
                 port="54321")

print("Conexion exitosa")

#SELECT * FROM categorias  // querry de ejemplo
#con.commit()  // Actualiza los cambios en la base de datos, 
#                   asi como los CREATE TABLE o UPDATES, etc


def InsertQuerry(text):
    cur = con.cursor()
    cur.execute(text)
    request = cur.fetchall()
    headers = []
#    for a in request:
#        headers.append(a[0])
#    print(tabulate(request, headers, tablefmt="psql"))
    print(request)

flag = True

while flag:
    opcion = input("Ingrese opcion\n1) Querry\n2)Exit\n")
    if opcion == "1":
        querry = input("Ingresar querry: ")
        InsertQuerry(querry)
    if opcion == "2":
        flag = False

con.close()

