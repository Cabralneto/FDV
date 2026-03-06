import pandas as pd


def normalize_columns(columns: list[str]) -> list[str]:
    return [c.strip().lower().replace(" ", "_") for c in columns]


def load_excel(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = normalize_columns(list(df.columns))
    return df
