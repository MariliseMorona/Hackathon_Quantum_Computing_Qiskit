import os
import pandas as pd
import numpy as np


def load_soil_data(path="data/crop.csv"):
    """
    Carrega dataset de solo com pH e label (cultura).
    - Se o arquivo não existir, cria um dataset sintético para demonstração.
    - Retorna X (Nx1 pH), y (0=milho, 1=soja) e df completo para visualização.
    """
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        # Dataset sintético: 40 amostras com pH entre 4.5 e 7.5
        rng = np.random.default_rng(42)
        ph_values = np.linspace(4.5, 7.5, 40) + rng.normal(0, 0.15, 40)
        labels = ["maize" if ph <= 6.0 else "soybean" for ph in ph_values]
        df = pd.DataFrame({"pH": ph_values, "label": labels})

    # Normalizar nomes de colunas comuns
    cols = {c.lower(): c for c in df.columns}
    ph_col = cols.get("pH".lower()) or cols.get("ph")
    label_col = cols.get("label") or cols.get("crop")

    if ph_col is None or label_col is None:
        raise KeyError("Colunas necessárias não encontradas (pH e label/crop).")

    # Mapear cultura para 0 = Milho, 1 = Soja (suporta variações)
    def map_crop(val: str) -> int:
        v = str(val).strip().lower()
        if v in {"maize", "corn", "milho"}:
            return 0
        if v in {"soy", "soybean", "soja"}:
            return 1
        # fallback por regra simples: pH <= 6 -> milho, pH > 6 -> soja
        return 0

    df["Crop"] = df[label_col].apply(map_crop)
    X = df[[ph_col]].to_numpy(dtype=float)
    y = df["Crop"].to_numpy(dtype=int)

    return X, y, df
