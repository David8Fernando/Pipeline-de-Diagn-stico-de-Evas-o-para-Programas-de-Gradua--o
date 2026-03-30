from pathlib import Path
from datetime import datetime

from src.ingestao import carregar_dados
from src.limpeza import limpar_dados
from src.validacao import validar_dataset
from src.transformacao import (
    criar_metricas,
    tabelas_intermediarias_frequencia,
    tabelas_intermediarias_matricula,
    tabelas_intermediarias_desempenho
)
from src.indicadores import gerar_indicadores
from src.carga_dados_sql import carregar_dados_consolidados_sql


# 📁 caminhos corretos
BASE_DIR = Path(__file__).resolve().parent
RAW_PATH = BASE_DIR / "data" / "raw"
REFINED_PATH = BASE_DIR / "data" / "refined"

REFINED_PATH.mkdir(parents=True, exist_ok=True)


def main():

    print("Procurando arquivos em:", RAW_PATH.resolve())

    arquivos = list(RAW_PATH.glob("dataset_*.csv"))

    if not arquivos:
        raise FileNotFoundError(f"Nenhum dataset encontrado em {RAW_PATH.resolve()}")

    # pega o mais recente
    arquivo = max(arquivos, key=lambda x: x.stat().st_mtime)

    print(f"Usando arquivo: {arquivo}")

    # 1. leitura
    df = carregar_dados(arquivo)

    # 2. validação
    validar_dataset(df)

    # 3. limpeza
    df = limpar_dados(df)

    # 4. transformações
    df_final = criar_metricas(df)
    df_matricula = tabelas_intermediarias_matricula(df)
    df_frequencia = tabelas_intermediarias_frequencia(df)
    df_desempenho = tabelas_intermediarias_desempenho(df)

    # 5. indicadores (REQUISITO)
    df_indicadores = gerar_indicadores(df)

    # 6. timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 7. exportação
    df_final.to_parquet(REFINED_PATH / f"consolidado_{timestamp}.parquet", index=False)
    df_matricula.to_parquet(REFINED_PATH / f"matricula_{timestamp}.parquet", index=False)
    df_frequencia.to_parquet(REFINED_PATH / f"frequencia_{timestamp}.parquet", index=False)
    df_desempenho.to_parquet(REFINED_PATH / f"desempenho_{timestamp}.parquet", index=False)
    df_indicadores.to_parquet(REFINED_PATH / f"indicadores_{timestamp}.parquet", index=False)

    # 8. sql
    df_sql = carregar_dados_consolidados_sql(df)

    print("Pipeline executado com sucesso!")
    print(df_sql.head())


if __name__ == "__main__":
    main()