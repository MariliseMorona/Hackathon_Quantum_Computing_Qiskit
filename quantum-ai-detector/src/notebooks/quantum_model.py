import numpy as np

# Tentar importar Qiskit
try:
    from qiskit import QuantumCircuit, Aer, execute
    QISKIT_AVAILABLE = True
except Exception:
    QISKIT_AVAILABLE = False

def plant_choice_qiskit(ph):
    theta = (ph - 4) / 4 * np.pi
    if QISKIT_AVAILABLE:
        qc = QuantumCircuit(1, 1)
        qc.ry(theta, 0)
        qc.measure(0, 0)
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()
        prob_0 = counts.get('0', 0)/1024
        prob_1 = counts.get('1', 0)/1024
        return np.array([prob_0, prob_1]), qc
    else:
        prob_0 = float(np.cos(theta/2) ** 2)
        prob_1 = float(np.sin(theta/2) ** 2)
        circuit_text = f"RY({theta:.3f}) on qubit 0\nMeasure"
        class SimpleCircuit:
            def __init__(self, text): self._text = text
            def draw(self): return self._text
        return np.array([prob_0, prob_1]), SimpleCircuit(circuit_text)

def plant_choice_2qubits(ph, N, N_max=100):
    """
    Codifica pH e Nitrogênio em 2 qubits.
    Retorna probabilidades e circuito (ou versão fallback textual se Qiskit não estiver disponível).
    """
    theta1 = (ph - 4) / 4 * np.pi
    theta2 = (N / N_max) * np.pi

    if QISKIT_AVAILABLE:
        from qiskit import QuantumCircuit, Aer, execute

        qc = QuantumCircuit(2, 2)
        qc.ry(theta1, 0)
        qc.ry(theta2, 1)
        qc.measure([0, 1], [0, 1])

        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()
        probs = {k: v / 1024 for k, v in counts.items()}

        return probs, qc
    else:
        # Fallback analítico simples
        prob_00 = np.cos(theta1/2)**2 * np.cos(theta2/2)**2
        prob_01 = np.cos(theta1/2)**2 * np.sin(theta2/2)**2
        prob_10 = np.sin(theta1/2)**2 * np.cos(theta2/2)**2
        prob_11 = np.sin(theta1/2)**2 * np.sin(theta2/2)**2

        probs = {"00": prob_00, "01": prob_01, "10": prob_10, "11": prob_11}

        # Circuito textual simples
        circuit_text = (
            "┌──────────────┐\n"
            f"│ RY({theta1:.3f}) │ — qubit 0 (pH)\n"
            f"│ RY({theta2:.3f}) │ — qubit 1 (Nitrogênio)\n"
            "└──────────────┘\n"
            "Measure: probs(q0,q1)"
        )

        class SimpleCircuit:
            def __init__(self, text):
                self._text = text
            def draw(self):
                return self._text

        qc = SimpleCircuit(circuit_text)
        return probs, qc
