from pathlib import Path
from datetime import datetime
import pandas as pd
from src.ingestao import carregar_dados
from src.limpeza import limpar_dados
from src.validacao import validar_dataset
from src.transformacao import criar_metricas, tabelas_intermediarias_frequencia, tabelas_intermediarias_matricula, tabelas_intermediarias_desempenho
from src.carga_dados_sql import carregar_dados_consolidados_sql 
DATA_PATH = Path("data")


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data"
OUTPUT_PATH = DATA_PATH / "refined"
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)



def main():

    

    print("Procurando em:", DATA_PATH.resolve())
    print("Arquivos encontrados:", list(DATA_PATH.glob("*")))


    arquivos = list(DATA_PATH.glob("dataset_*.csv"))

    if not arquivos:
        raise FileNotFoundError(f"Nenhum dataset encontrado em {DATA_PATH.resolve()}")

    arquivo = max(arquivos, key=lambda x: x.stat().st_mtime)

    print(f"Usando arquivo: {arquivo}")
    
    #1 - Leitura arquivo
    df = carregar_dados(arquivo)

    #2 - Validação
    validar_dataset(df)

    #3 - limpeza 
    df = limpar_dados(df)

    #4 - Transformação
    df_final = criar_metricas(df)

    #5 - Tabelas intermediárias
    df_matricula = tabelas_intermediarias_matricula(df)
    df_frequencia = tabelas_intermediarias_frequencia(df)
    df_desempenho = tabelas_intermediarias_desempenho(df)

    #5 - Timestamp para rastreabilidade
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    #6 - Exportação para PowerBI
    df_final.to_parquet(OUTPUT_PATH / f"consolidado_{timestamp}.parquet", index=False)
    df_matricula.to_parquet(OUTPUT_PATH / f"matricula_{timestamp}.parquet", index=False)
    df_frequencia.to_parquet(OUTPUT_PATH / f"frequencia_{timestamp}.parquet", index=False)
    df_desempenho.to_parquet(OUTPUT_PATH / f"desempenho_{timestamp}.parquet", index=False)

    #7 - Exportação para SQL 
    df_consolidado_sql = carregar_dados_consolidados_sql(df)

    print("Pipeline executado com sucesso!")
    print("Consolidado SQL:")
    print(df_consolidado_sql.head())

if __name__ == "__main__":
    main()