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