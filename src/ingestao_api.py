import requests
import json
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

from src.config import RAW_PATH

load_dotenv()


def baixar_dados_api(project_id):
    token = os.getenv("DATAMISSION_API_TOKEN")

    if not token:
        raise ValueError("Token não encontrado no .env")

    url = f"https://api.datamission.com.br/projects/{project_id}/dataset?format=csv"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 📁 salva no lugar correto
    csv_path = RAW_PATH / f"dataset_{project_id}_{timestamp}.csv"

    with open(csv_path, "wb") as f:
        f.write(response.content)

    # 📄 metadata
    metadata = {
        "project_id": project_id,
        "timestamp": timestamp,
        "headers": dict(response.headers)
    }

    metadata_path = RAW_PATH / f"metadata_{project_id}_{timestamp}.json"

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    # 📊 schema
    df_sample = pd.read_csv(csv_path, nrows=100)

    def map_dtype(dtype):
        if pd.api.types.is_integer_dtype(dtype):
            return "integer"
        elif pd.api.types.is_float_dtype(dtype):
            return "float"
        else:
            return "string"

    schema = []
    for col in df_sample.columns:
        series = df_sample[col]

        schema.append({
            "column": col,
            "type": map_dtype(series.dtype),
            "nulls": int(series.isnull().sum()),
            "unique": int(series.nunique())
        })

    schema_path = RAW_PATH / f"schema_{project_id}_{timestamp}.json"

    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=4)

    print(f"✅ Dados salvos em: {csv_path}")

    return csv_path