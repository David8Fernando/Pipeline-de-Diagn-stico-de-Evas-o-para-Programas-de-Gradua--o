from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data"
RAW_PATH = DATA_PATH / "raw"
STAGING_PATH = DATA_PATH / "staging"
REFINED_PATH = DATA_PATH / "refined"

# cria tudo automaticamente
for path in [DATA_PATH, RAW_PATH, STAGING_PATH, REFINED_PATH]:
    path.mkdir(parents=True, exist_ok=True)