from flask import Flask, request, jsonify
from flask_cors import CORS
from simulator import simular

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Simulador 5G funcionando"

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.json  # ✅ primero obtener data

    antennas = data["antennas"]
    fc = data["frequency"]

    # ✅ obtener modelo (con default)
    modelo = data.get("modelo", "UMI")

    # ✅ una sola llamada
    resultados = simular(antennas, fc, modelo)

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=True)
