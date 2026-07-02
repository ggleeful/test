from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/dni")
def consultar_dni():
    dni = request.args.get("dni")
    debug = request.args.get("debug")

    if not dni:
        return jsonify({"error": "Debe enviar el parámetro dni"}), 400

    url = f"https://www.cuitonline.com/search/{dni}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "No se pudo acceder a la página"}), 500

    soup = BeautifulSoup(response.text, "html.parser")

    # Extraer nombre y CUIT según el HTML que compartiste
    nombre_tag = soup.find("h2", class_="denominacion")
    cuit_tag = soup.find("span", class_="cuit")

    nombre = nombre_tag.text.strip() if nombre_tag else "No encontrado"
    cuit = cuit_tag.text.strip() if cuit_tag else "No encontrado"

    resultado = {
        "dni": dni,
        "nombre": nombre,
        "cuit": cuit
    }

    # Si se pasa debug=true, incluir el HTML bruto
    if debug == "true":
        resultado["html_raw"] = response.text

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
