import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="SRINK",
        password="Vayneadc2022",
        database="scraping_ml"
    )
    if conexion.is_connected():
        #print("Conectado a la base de datos")
        cursor = conexion.cursor()
        cursor.execute("select database();")
        row = cursor.fetchone()
        print("Conectado a la base de datos:{} ". format(row))
        info = conexion.get_server_info()
        print("MySQL Server version ", info)
except Exception as ex:
    print(ex)


# Función para insertar los datos en la tabla correspondiente de la base de datos
def insertar_datos(conexion, producto, precios, urls):
    try:
        # Se crea el cursor para ejecutar las consultas SQL
        cursor = conexion.cursor()

        # Se define la consulta SQL para insertar los datos en la tabla correspondiente
        consulta = "INSERT INTO data_ml (producto, precio, url) VALUES (%s, %s, %s)"

        # Se itera sobre los datos extraídos para insertarlos en la tabla
        for i in range(len(producto)):
            datos = (producto[i], precios[i], urls[i])

            # Se verifica que los datos no hayan sido insertados previamente
            cursor.execute("SELECT * FROM data_ml WHERE producto=%s AND precio=%s AND url=%s", datos)
            resultado = cursor.fetchone()
            if resultado is None:
                cursor.execute(consulta, datos)

        # Se confirman los cambios en la base de datos
        conexion.commit()

        # Se cierra el cursor
        cursor.close()

        print("Datos insertados en la base de datos")

    except Exception as ex:
        print(ex)


####

