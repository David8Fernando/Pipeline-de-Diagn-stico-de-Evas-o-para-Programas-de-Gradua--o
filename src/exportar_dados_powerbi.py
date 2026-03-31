from datetime import datetime
from src.config import REFINED_PATH


def exportar_dados(df, nome):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    parquet_path = REFINED_PATH / f"{nome}_{timestamp}.parquet"
    csv_path = REFINED_PATH / f"{nome}_{timestamp}.csv"

    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False)

    print(f"Exportado: {nome}")

    return parquet_path, csv_path