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
    data = request.json

    antennas = data["antennas"]
    fc = data["frequency"]

    resultado = simular(antennas, fc)

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)
