"""Modelos clássicos simples para decisão de plantio.

Este módulo implementa uma regra de decisão baseada em limiar de pH
para classificar entre Milho (0) e Soja (1). É intencionalmente
simples para servir de comparação com o modelo quântico.
"""

import numpy as np

def classical_decision(X: np.ndarray) -> np.ndarray:
    """Aplica uma regra de limiar no pH para decidir a cultura.

    - Se `pH > 6.0` → Soja (`1`)
    - Caso contrário → Milho (`0`)

    Parâmetros:
    - X: array de features com formato `(n_amostras, n_features)`,
      onde `X[:, 0]` é o pH.

    Retorno:
    - Array de inteiros (`0` ou `1`) com formato `(n_amostras,)`.
    """
    # Usa a primeira coluna como pH; garante saída inteira booleana (0/1)
    return (X[:, 0] > 6.0).astype(int)

def classical_probs(X: np.ndarray) -> np.ndarray:
    """Gera probabilidades compatíveis com visualização para Milho e Soja.

    Esta função converte a decisão binária em um vetor de probabilidades
    simples, útil para gráficos de barras no dashboard:

    - Se decisão for Milho (`0`): prob = [1.0, 0.0]
    - Se decisão for Soja  (`1`): prob = [0.0, 1.0]

    Parâmetros:
    - X: array de features com formato `(n_amostras, n_features)`.

    Retorno:
    - Array de floats com formato `(n_amostras, 2)` no ordenamento
      `[prob_Milho, prob_Soja]`.
    """
    decisions = classical_decision(X)
    # Empilha o complementar e a própria decisão para formar [p_milho, p_soja]
    return np.stack([1 - decisions, decisions], axis=1)
