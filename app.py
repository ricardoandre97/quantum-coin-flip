from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pennylane as qml
import numpy as np

app = Flask(__name__)
CORS(app)

# Devices
dev_analytic = qml.device("default.qubit", wires=1, shots=None)  # For qml.state()
dev_shot = qml.device("default.qubit", wires=1, shots=1)         # For measurement


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/prepare")
def prepare():
    @qml.qnode(dev_analytic)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.state()

    state = circuit()

    code = """@qml.qnode(dev_analytic)
def circuit():
    qml.Hadamard(wires=0)
    return qml.state()"""

    return jsonify({
        "state": "state: array([0.70710678+0.j 0.70710678+0.j])",
        "code": code,
        "tip": "This puts the qubit into a superposition: equal chance of |0⟩ and |1⟩."
    })


@app.route("/measure")
def measure():
    @qml.qnode(dev_shot)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(0))

    result = circuit()  # Will be either +1 or -1
    label = "HEADS" if result == 1 else "TAILS"

    code = """@qml.qnode(dev_shot)
def circuit():
    qml.Hadamard(wires=0)
    return qml.sample(qml.PauliZ(0))"""

    return jsonify({
        "result": label,
        "code": code,
        "tip": "We measured in the Z basis. The qubit collapsed and will stay this way until reset."
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0")