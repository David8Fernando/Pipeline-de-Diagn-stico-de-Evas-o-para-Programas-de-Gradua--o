import pandas as pd

def limpar_dados(df):
    # 1. Padronizar nomes de colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 2. Remover duplicados
    df = df.drop_duplicates()

    # 3. Converter datas
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # 4. Remover colunas totalmente nulas
    df = df.dropna(axis=1, how="all")

    # 5. Tratar colunas parcialmente nulas
    for col in df.columns:
        if df[col].isnull().any():
            
            # Se for numérica → preencher com média
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())

            # Se for texto → preencher com "desconhecido"
            else:
                df[col] = df[col].fillna("desconhecido")

    return df