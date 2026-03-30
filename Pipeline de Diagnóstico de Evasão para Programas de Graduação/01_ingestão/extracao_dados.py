import requests
import json
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DATAMISSION_API_TOKEN")

if not token:
    raise ValueError("Token de API não encontrado. Verifique o arquivo .env e a variável DATAMISSION_API_TOKEN.")


# ===== CONFIG =====
project_id = "e21f7967-1182-44a9-b29e-6e8833f294e7"

url = f"https://api.datamission.com.br/projects/{project_id}/dataset?format=csv"
headers = {"Authorization": f"Bearer {token}"}

# ===== REQUEST =====
response = requests.get(url, headers=headers)
response.raise_for_status()

# ===== TIMESTAMP (pra versionamento) =====
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ===== SALVAR CSV =====
csv_filename = f"dataset_{project_id}_{timestamp}.csv"

with open(csv_filename, "wb") as file:
    file.write(response.content)

# ===== CAPTURAR HEADERS =====
response_headers = dict(response.headers)

# ===== SALVAR METADADOS =====
metadata = {
    "project_id": project_id,
    "download_timestamp": timestamp,
    "url": url,
    "status_code": response.status_code,
    "headers": response_headers
}

metadata_filename = f"metadata_{project_id}_{timestamp}.json"

with open(metadata_filename, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

# ===== LOG =====
print(f"✅ CSV salvo em: {csv_filename}")
print(f"📄 Metadados salvos em: {metadata_filename}")



import pandas as pd

df = pd.read_csv(csv_filename, nrows=100)  # lê só as primeiras linhas

def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "integer"
    elif pd.api.types.is_float_dtype(dtype):
        return "float"
    elif pd.api.types.is_bool_dtype(dtype):
        return "boolean"
    else:
        return "string"
    

schema = []

for col in df.columns:
    series = df[col]

    schema.append({
        "column": col,
        "type": map_dtype(series.dtype),
        "null_count": int(series.isnull().sum()),
        "unique_values": int(series.nunique()),
        "sample_value": str(series.dropna().iloc[0]) if not series.dropna().empty else ""
    })


    import json

schema_json_file = f"schema_{project_id}_{timestamp}.json"

with open(schema_json_file, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=4, ensure_ascii=False)

schema_md_file = f"schema_{project_id}_{timestamp}.md"

with open(schema_md_file, "w", encoding="utf-8") as f:
    f.write("# 📊 Schema Documentation\n\n")
    f.write(f"Arquivo: {csv_filename}\n\n")

    f.write("| Coluna | Tipo | Nulos | Únicos | Exemplo |\n")
    f.write("|--------|------|-------|--------|---------|\n")

    for col in schema:
        f.write(f"| {col['column']} | {col['type']} | {col['null_count']} | "
                f"{col['unique_values']} | {col['sample_value']} |\n")