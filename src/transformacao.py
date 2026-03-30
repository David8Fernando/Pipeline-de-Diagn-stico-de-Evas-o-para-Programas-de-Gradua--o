import pandas as pd
def criar_metricas(df):
    df["ano"] = df["timestamp"].dt.year
    df["mes"] = df["timestamp"].dt.month

    df_consolidado = df.groupby("course_name").agg(
        total_alunos=("student_id", "nunique"),
        frequencia_media=("attendance_rate", "mean"),
        desempenho_medio=("grade_point_average", "mean")
    ).reset_index()

    return df_consolidado


def tabelas_intermediarias_matricula(df):
# tabela de matrícula
    df_matricula = df[[
    "student_id",
    "course_name",
    "enrollment_status",
    "timestamp"
]].drop_duplicates()
    return df_matricula

def tabelas_intermediarias_frequencia(df):
# tabela de frequencia
    df_frequencia = df[[
    "student_id",
    "course_name",
    "attendance_rate"
]].drop_duplicates()
    
    return df_frequencia
def tabelas_intermediarias_desempenho(df):
# tabela de desempenho
    df_desempenho = df[[
    "student_id",
    "course_name",
    "grade_point_average"
]].drop_duplicates()
    return df_desempenho


# src/validacao.py

import pandas as pd

COLUNAS_ESPERADAS = {
    "student_id": "object",
    "timestamp": "object",
    "course_name": "object",
    "enrollment_status": "object",
    "grade_point_average": "float64",
    "attendance_rate": "int64",
    "scholarship_percent": "int64"
}

def validar_dataset(df):
    # 1. Linhas mínimas
    if len(df) < 100:
        raise ValueError("Dataset com poucas linhas")

    # 2. Colunas esperadas
    colunas_df = set(df.columns)
    colunas_esperadas = set(COLUNAS_ESPERADAS.keys())

    if colunas_df != colunas_esperadas:
        raise ValueError(f"Colunas divergentes: {colunas_df}")

    # 3. Tipos (opcional mais rígido)
    for col, tipo in COLUNAS_ESPERADAS.items():
        if col in df.columns:
            if df[col].dtype != tipo:
                print(f"Aviso: tipo divergente em {col}")

    return True



def criar_indicadores(df):
    df["aprovado"] = df["grade_point_average"] >= 6
    df["evasao_risco"] = (df["attendance_rate"] < 75)

    df_indicadores = df.groupby("course_name").agg(
        total_alunos=("student_id", "nunique"),
        taxa_aprovacao=("aprovado", "mean"),
        frequencia_media=("attendance_rate", "mean"),
        desempenho_medio=("grade_point_average", "mean"),
        risco_evasao=("evasao_risco", "mean")
    ).reset_index()

    return df_indicadores