# src/quantum_model.py
import pennylane as qml
from pennylane import numpy as np

# Dispositivo quântico
n_qubits = 1
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def plant_choice(ph):
    """
    Codifica pH em rotação RY e retorna probabilidades de Milho | Soja
    """
    # Normaliza pH para [0, pi]
    theta = (ph - 4) / 4 * np.pi
    qml.RY(theta, wires=0)
    return qml.probs(wires=0)
