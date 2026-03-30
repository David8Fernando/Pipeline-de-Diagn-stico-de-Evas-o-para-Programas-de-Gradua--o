import pandas as pd

def limpar_dados(df):
    print(f"Shape inicial: {df.shape}")

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
    colunas_antes = df.shape[1]
    df = df.dropna(axis=1, how="all")
    colunas_depois = df.shape[1]

    print(f"Colunas removidas (100% nulas): {colunas_antes - colunas_depois}")

    # 5. Tratar colunas parcialmente nulas
    for col in df.columns:
        if df[col].isnull().any():

            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna("desconhecido")

    print(f"Shape final: {df.shape}")

    return df