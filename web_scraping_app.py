from flask import Flask, jsonify, request, render_template, Response
import json
from functions import todosProductos, limite_producto
import requests
from mysql_utils import conexion, insertar_datos

app = Flask(__name__)

@app.route('/mercadoLibre', methods=["GET", "POST"])
def mercadoLibre():
    try:
        data = request.form.to_dict()  # Se obtienen los datos enviados por el cliente
        print(data)

        if 'limite' not in data:
            producto, precios, urls = todosProductos(data['producto'])
        else:
            producto, precios, urls = limite_producto(data['producto'], int(data['limite']))

        insertar_datos(conexion, producto, precios, urls)

        return jsonify({"datos": {"producto": producto, "precios": precios, "urls": urls}})
    except Exception as ex:
        print(ex)
        return "verifique los datos enviados"

@app.route('/descargarInfo', methods=["GET", "POST"])
def descargarInfo():
    try:
        producto = request.form['producto']
        limite = request.form['limite']
        r = requests.post("http://localhost:4000/mercadoLibre", data={"producto": producto, "limite": limite})
        print(r.status_code)
        if r.status_code == 200:
            data = json.loads(r.text)
            t = ""
            for i, j, z in zip(data["datos"]["producto"], data["datos"]["precios"], data["datos"]["urls"]):
                t += f"{i} | {j} | {z}\n"

            return Response(
                t,
                mimetype="text",
                #headers={
                    #"Content-disposition": "attachment; filename=datos.txt"
                #}
            )
            
    except Exception as ex:
        print(ex)
        return render_template('index.html')

@app.route("/borrar-datos", methods=["DELETE"])
def borrar_datos():
    try:
        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM data_ml")
            conexion.commit()
            cursor.close()
            return "Datos eliminados correctamente", 200
    except Exception as ex:
        print(ex)
        return "Error al eliminar los datos", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)



