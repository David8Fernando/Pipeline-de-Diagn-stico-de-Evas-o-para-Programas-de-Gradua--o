import sqlite3
import pandas as pd

def carregar_dados_consolidados_sql(df):
    with sqlite3.connect("dados.db") as conn:

        # 1. Carregar tabela base
        df.to_sql("base", conn, if_exists="replace", index=False)

        # 2. Garantir recriação da view (idempotência)
        conn.execute("DROP VIEW IF EXISTS vw_curso_consolidado")

        conn.execute("""
        CREATE VIEW vw_curso_consolidado AS
        SELECT 
            course_name,
            COUNT(DISTINCT student_id) AS total_alunos,
            AVG(attendance_rate) AS frequencia_media,
            AVG(grade_point_average) AS desempenho_medio,
            AVG(scholarship_percent) AS bolsa_media
        FROM base
        GROUP BY course_name
        """)

        # 3. Ler resultado
        df_final = pd.read_sql("SELECT * FROM vw_curso_consolidado", conn)

    return df_final