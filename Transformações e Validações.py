import pandas as pd

from src.ingestao_api import baixar_dados_api
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
from src.exportar_dados_powerbi import exportar_dados
from src.carga_dados_sql import carregar_dados_consolidados_sql


PROJECT_ID = "e21f7967-1182-44a9-b29e-6e8833f294e7"


def main():

    # 1. EXTRAÇÃO AUTOMÁTICA
    arquivo = baixar_dados_api(PROJECT_ID)

    # 2. LEITURA 
    df = carregar_dados(arquivo)

    # 3. VALIDAÇÃO
    validar_dataset(df)

    # 4. LIMPEZA
    df = limpar_dados(df)

    # 5. TRANSFORMAÇÕES
    df_consolidado = criar_metricas(df)
    df_matricula = tabelas_intermediarias_matricula(df)
    df_frequencia = tabelas_intermediarias_frequencia(df)
    df_desempenho = tabelas_intermediarias_desempenho(df)

    # 6. INDICADORES 
    df_indicadores = gerar_indicadores(df)

    # 7. EXPORTAÇÃO POWER BI 
    exportar_dados(df_consolidado, "consolidado")
    exportar_dados(df_matricula, "matricula")
    exportar_dados(df_frequencia, "frequencia")
    exportar_dados(df_desempenho, "desempenho")
    exportar_dados(df_indicadores, "indicadores")

    # 8. SQL
    df_sql = carregar_dados_consolidados_sql(df)

    print(" PIPELINE EXECUTADA COM SUCESSO")
    print(df_sql.head())


if __name__ == "__main__":
    main()