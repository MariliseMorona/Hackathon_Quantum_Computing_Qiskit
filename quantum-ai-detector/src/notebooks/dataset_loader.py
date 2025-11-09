import os
import pandas as pd
import numpy as np

TARGET_DIR = "../data"
TARGET_FILE = os.path.join(TARGET_DIR, "crop.csv")

def load_data(path: str = TARGET_FILE):
    """Carrega dataset de solo e retorna X (pH + Nitrogênio), y (0=Milho, 1=Soja) e df completo."""
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = _synthetic_dataset()

    # Normalizar nomes de colunas
    cols = {c.lower(): c for c in df.columns}
    ph_col = cols.get("pH".lower()) or cols.get("ph") or cols.get("soil_ph")
    label_col = cols.get("label") or cols.get("crop") or cols.get("cultura")

    if ph_col is None or label_col is None:
        raise KeyError("Colunas necessárias não encontradas (pH e label/crop).")

    # Garantir coluna Nitrogênio
    if "Nitrogen" not in df.columns:
        df["Nitrogen"] = np.random.uniform(0, 100, len(df))  # valor sintético

    # Mapear cultura para 0 = Milho, 1 = Soja
    def map_crop(val: str) -> int:
        v = str(val).strip().lower()
        if v in {"maize", "corn", "milho"}:
            return 0
        if v in {"soy", "soybean", "soja"}:
            return 1
        return 0

    df["Crop"] = df[label_col].apply(map_crop)

    # Features: pH + Nitrogênio
    X = df[[ph_col, "Nitrogen"]].to_numpy(dtype=float)
    y = df["Crop"].to_numpy(dtype=int)

    return X, y, df

def _synthetic_dataset() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    ph_values = np.linspace(4.5, 7.5, 40) + rng.normal(0, 0.15, 40)
    labels = ["maize" if ph <= 6.0 else "soybean" for ph in ph_values]
    nitrogen = np.random.uniform(0, 100, 40)
    return pd.DataFrame({"pH": ph_values, "Nitrogen": nitrogen, "label": labels})

if __name__ == "__main__":
    X, y, df = load_data()
    print(df.head())
