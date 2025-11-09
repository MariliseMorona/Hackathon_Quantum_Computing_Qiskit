# app.py
import streamlit as st
import pandas as pd
import numpy as np
from src.dataset_loader import load_soil_data
from src.classical_model import classical_decision, classical_probs
from src.quantum_model import plant_choice

st.set_page_config(page_title="🌱 Decisão de Plantio Quântico", layout="centered")

st.title("🌱 Decisão de Plantio: Milho vs Soja")
st.caption("Experimento quântico simples usando pH do solo como entrada.")

# --- Carregar dataset ---
X, y, df = load_soil_data()
st.subheader("Dataset de Solo")
st.dataframe(df)

# --- Seleção de amostra ---
sample_idx = st.slider("Selecione uma amostra do solo", 0, len(df)-1, 0)
ph_sample = X[sample_idx, 0]

st.write(f"Você selecionou a amostra #{sample_idx} com pH = {ph_sample:.2f}")

# --- Probabilidade Clássica ---
st.subheader("Modelo Clássico (Threshold)")
prob_classical = classical_probs(X[sample_idx:sample_idx+1])[0]
st.write(f"Probabilidades de plantio (Milho | Soja): {prob_classical}")
st.bar_chart(prob_classical)

# --- Probabilidade Quântica ---
st.subheader("Modelo Quântico (1 qubit)")

prob_quantum = plant_choice(ph_sample)
st.write(f"Probabilidades de plantio (Milho | Soja) para pH={ph_sample:.2f}: {prob_quantum}")
st.bar_chart(prob_quantum)

# --- Circuit Board ---
st.subheader("Circuito Quântico Visual")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(4,1))
ax.hlines(y=0, xmin=0, xmax=1, color="black", linewidth=2)
ax.plot(0.5, 0, 'o', markersize=20, color='orange')
ax.text(0.5, 0.2, f"pH = {ph_sample:.2f}", ha='center')
ax.set_xlim(0,1)
ax.set_ylim(-0.5, 0.5)
ax.axis("off")
ax.set_title("Qubit representando decisão de plantio")
st.pyplot(fig)
