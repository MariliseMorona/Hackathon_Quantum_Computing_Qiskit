"""Modelo quântico para decisão de plantio.

Este módulo implementa uma codificação simples de uma variável contínua
(pH) em um ângulo de rotação `RY(theta)` em um qubit. Quando o Qiskit
está disponível, o circuito é simulado; caso contrário, é usada uma
aproximação analítica com representação textual do circuito.
"""

import numpy as np

# Tentar importar Qiskit para simulação real; caso falhe, usa fallback.
try:
    from qiskit import QuantumCircuit, Aer, execute
    QISKIT_AVAILABLE = True
except Exception:
    QISKIT_AVAILABLE = False

def plant_choice_qiskit(ph: float):
    """Calcula probabilidades de plantio usando um circuito de 1 qubit.

    Mapeamento: `ph` → `theta` por uma normalização linear simples
    entre 4 e 8, escalando para `pi`:

    `theta = (ph - 4) / 4 * pi`

    - Com Qiskit: cria `QuantumCircuit(1,1)`, aplica `RY(theta)` e mede;
      probabilidades são estimadas via simulação (shots=1024).
    - Sem Qiskit: usa a fórmula analítica das amplitudes de `RY`:
      `p(0) = cos^2(theta/2)`, `p(1) = sin^2(theta/2)` e retorna um
      objeto simples com `.draw()` textual.

    Parâmetros:
    - ph: valor de pH (float).

    Retorno:
    - Tuple `(probs, qc)` onde `probs` é `np.array([p_milho, p_soja])`
      e `qc` é o circuito (real ou textual).
    """
    theta = (ph - 4) / 4 * np.pi

    if QISKIT_AVAILABLE:
        # Circuito de 1 qubit com medição em 1 bit clássico
        qc = QuantumCircuit(1, 1)
        qc.ry(theta, 0)
        qc.measure(0, 0)

        # Simulação via backend de QASM
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()

        # Probabilidades normalizadas pelo número de shots
        prob_0 = counts.get('0', 0) / 1024
        prob_1 = counts.get('1', 0) / 1024
        return np.array([prob_0, prob_1]), qc
    else:
        # Cálculo analítico direto das probabilidades da rotação RY
        prob_0 = float(np.cos(theta / 2) ** 2)
        prob_1 = float(np.sin(theta / 2) ** 2)

        # Representação textual mínima do circuito para visualização
        circuit_text = f"RY({theta:.3f}) on qubit 0\nMeasure"

        class SimpleCircuit:
            def __init__(self, text):
                self._text = text
            def draw(self):
                return self._text

        return np.array([prob_0, prob_1]), SimpleCircuit(circuit_text)

def plant_choice_2qubits(ph: float, N: float, N_max: float = 100):
    """Codifica pH e Nitrogênio em 2 qubits e obtém probabilidades.

    - Qubit 0 (pH): `theta1 = (ph - 4) / 4 * pi`
    - Qubit 1 (Nitrogênio): `theta2 = (N / N_max) * pi`

    - Com Qiskit: simula o circuito e retorna contagens normalizadas.
    - Sem Qiskit: calcula `p(b0,b1)` analiticamente e retorna circuito
      textual com `.draw()`.

    Parâmetros:
    - ph: pH do solo.
    - N: nível de Nitrogênio.
    - N_max: valor máximo de referência para normalização de N.

    Retorno:
    - Tuple `(probs, qc)` onde `probs` é um dict `{"00": p00, ...}` e
      `qc` é o circuito (real ou textual).
    """
    theta1 = (ph - 4) / 4 * np.pi
    theta2 = (N / N_max) * np.pi

    if QISKIT_AVAILABLE:
        # Import local para evitar custo quando Qiskit não está disponível
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
        # Fallback analítico assumindo independência das rotações
        prob_00 = np.cos(theta1 / 2) ** 2 * np.cos(theta2 / 2) ** 2
        prob_01 = np.cos(theta1 / 2) ** 2 * np.sin(theta2 / 2) ** 2
        prob_10 = np.sin(theta1 / 2) ** 2 * np.cos(theta2 / 2) ** 2
        prob_11 = np.sin(theta1 / 2) ** 2 * np.sin(theta2 / 2) ** 2

        probs = {"00": prob_00, "01": prob_01, "10": prob_10, "11": prob_11}

        # Circuito textual simples para visualização no dashboard
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
