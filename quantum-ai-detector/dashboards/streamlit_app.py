import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# Garantir que src/notebooks esteja no sys.path
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[1]
_NOTEBOOKS_DIR = _ROOT / "src" / "notebooks"
if str(_NOTEBOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(_NOTEBOOKS_DIR))

from dataset_loader import load_data
from classical_model import classical_decision, classical_probs
from quantum_model import plant_choice_qiskit, plant_choice_2qubits

# ---------------- Streamlit ----------------
st.set_page_config(page_title="🌱 Decisão de Plantio Quântico", layout="centered")
st.title("🌱 Decisão de Plantio: Milho vs Soja")
st.caption("Experimento quântico usando pH e Nitrogênio do solo como entrada.")

# --- Carregar dataset ---
X, y, df = load_data()
st.subheader("Dataset de Solo")
st.dataframe(df)

# --- Seleção de amostra ---
sample_idx = st.slider("Selecione uma amostra do solo", 0, len(df)-1, 0)
ph_sample = X[sample_idx, 0]
N_sample = X[sample_idx, 1]
st.write(f"Você selecionou a amostra #{sample_idx}: pH={ph_sample:.2f}, Nitrogênio={N_sample:.2f}")

# --- Modelo Clássico ---
st.subheader("Modelo Clássico (Threshold/Árvore)")
_t0_class = time.perf_counter()
prob_classical = classical_probs(X[sample_idx:sample_idx+1])[0]
_t_class_ms = (time.perf_counter() - _t0_class) * 1000
st.write(f"Probabilidades de plantio (Milho | Soja): {prob_classical}")
st.bar_chart(prob_classical)

# --- Modelo Quântico 1 qubit ---
st.subheader("Modelo Quântico (1 qubit - pH)")
_t0_q1 = time.perf_counter()
prob_q1, qc1 = plant_choice_qiskit(ph_sample)
_t_q1_ms = (time.perf_counter() - _t0_q1) * 1000
st.write(f"Probabilidades (Milho | Soja): {prob_q1}")
st.text(qc1.draw())

# Mini-circuito visual
fig, ax = plt.subplots(figsize=(4,1))
ax.hlines(y=0, xmin=0, xmax=1, color="black", linewidth=2)
ax.plot(0.5, 0, 'o', markersize=20, color='orange')
ax.text(0.5, 0.2, f"pH = {ph_sample:.2f}", ha='center')
ax.set_xlim(0,1); ax.set_ylim(-0.5,0.5)
ax.axis("off")
ax.set_title("Qubit codificando pH")
st.pyplot(fig)

# --- Modelo Quântico 2 qubits ---
st.subheader("Modelo Quântico (2 qubits - pH + Nitrogênio)")
_t0_q2 = time.perf_counter()
probs_2q, qc2 = plant_choice_2qubits(ph_sample, N_sample)
_t_q2_ms = (time.perf_counter() - _t0_q2) * 1000
st.write("Probabilidades de cada estado (00,01,10,11):", probs_2q)
st.text(qc2.draw())

# Mini-circuito visual
fig2, ax2 = plt.subplots(figsize=(4,2))
ax2.hlines(y=[0,1], xmin=0, xmax=1, color="black", linewidth=2)
ax2.plot(0.5, 0, 'o', markersize=20, color='orange')  # qubit 0 (pH)
ax2.plot(0.5, 1, 'o', markersize=20, color='green')   # qubit 1 (Nitrogênio)
ax2.text(0.5, 0.2, f"pH = {ph_sample:.2f}", ha='center')
ax2.text(0.5, 1.2, f"N = {N_sample:.2f}", ha='center')
ax2.set_xlim(0,1); ax2.set_ylim(-0.5,1.5)
ax2.axis("off")
ax2.set_title("Qubits codificando pH e Nitrogênio")
st.pyplot(fig2)

# --- Métricas de Acurácia ---
st.subheader("Acurácia no Dataset")
# Clássico: decisão pelo limiar em todo o dataset
acc_class = float(np.mean(classical_decision(X) == y))

# Quântico 1 qubit: usa fórmula analítica do RY para eficiência
theta_all = (X[:, 0] - 4) / 4 * np.pi
prob1_all = np.sin(theta_all / 2) ** 2  # p(Soja)
pred_q1 = (prob1_all >= 0.5).astype(int)
acc_q1 = float(np.mean(pred_q1 == y))

col_acc1, col_acc2 = st.columns(2)
col_acc1.metric("Acurácia Clássico", f"{acc_class*100:.1f}%")
col_acc2.metric("Acurácia Quântico 1 qubit", f"{acc_q1*100:.1f}%")

st.caption("A acurácia quântica foi calculada analiticamente (sem simulação) para performance.")

# --- Métricas de Tempo ---
st.subheader("Métricas de Tempo")
col1, col2, col3 = st.columns(3)
col1.metric("Clássico", f"{_t_class_ms:.2f} ms")
col2.metric("Quântico 1 qubit", f"{_t_q1_ms:.2f} ms")
col3.metric("Quântico 2 qubits", f"{_t_q2_ms:.2f} ms")
