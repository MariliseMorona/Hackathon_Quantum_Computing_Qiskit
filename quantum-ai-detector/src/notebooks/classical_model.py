# src/classical_model.py
import numpy as np

def classical_decision(X):
    """
    Regra simples: pH > 6 -> Soja (1), pH <= 6 -> Milho (0)
    """
    return (X[:,0] > 6).astype(int)

def classical_probs(X):
    """
    Probabilidades simuladas para visualização
    """
    return np.stack([1 - classical_decision(X), classical_decision(X)], axis=1)
