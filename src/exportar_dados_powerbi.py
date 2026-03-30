import pandas as pd

from pathlib import Path
from datetime import datetime

def exportar_dados(df, nome_arquivo):
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_PATH = BASE_DIR / "data" / "refined"
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_parquet = OUTPUT_PATH / f"{nome_arquivo}_{timestamp}.parquet"
    file_csv = OUTPUT_PATH / f"{nome_arquivo}_{timestamp}.csv"

    df.to_parquet(file_parquet, index=False)
    df.to_csv(file_csv, index=False)

    return file_parquet, file_csv