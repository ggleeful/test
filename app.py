from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/dni")
def consultar_dni():
    dni = request.args.get("dni")
    debug = request.args.get("debug")  # nuevo parámetro opcional

    if not dni:
        return jsonify({"error": "Debe enviar el parámetro dni"}), 400

    url = f"https://www.cuitonline.com/persona/dni/{dni}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "No se pudo acceder a la página"}), 500

    soup = BeautifulSoup(response.text, "html.parser")

    nombre_tag = soup.find("h1")
    cuit_tag = soup.find("div", class_="cuit")

    nombre = nombre_tag.text.strip() if nombre_tag else "No encontrado"
    cuit = cuit_tag.text.strip() if cuit_tag else "No encontrado"

    # Si debug está activado, devolver también el HTML bruto
    if debug == "true":
        return jsonify({
            "dni": dni,
            "nombre": nombre,
            "cuit": cuit,
            "html_raw": response.text  # muestra todo el HTML obtenido
        })

    return jsonify({
        "dni": dni,
        "nombre": nombre,
        "cuit": cuit
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
