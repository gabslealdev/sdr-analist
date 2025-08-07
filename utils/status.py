import streamlit as st
import pandas as pd


def status_geral(df: pd.DataFrame):
    """
    Exibe o status geral da base com as métricas:
    - Total de LEADS
    - ACIONADOS (com qualquer data de acionamento preenchida)
    - COBERTURA (ACIONADOS / LEADS)
    """
    st.subheader("📊 Status Geral da Base")

    total_leads = len(df)

    data_cols = [
        'DATA DO ACIONAMENTO I',
        'DATA DO ACIONAMENTO II',
        'DATA DO ACIONAMENTO III',
        'DATA DO ACIONAMENTO IV'
    ]

    acionados = df[data_cols].notnull().any(axis=1).sum()

    cobertura = round((acionados / total_leads) * 100, 1) if total_leads > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("LEADS", f"{total_leads}")
    col2.metric("ACIONADOS", f"{acionados}")
    col3.metric("COBERTURA", f"{cobertura} %")
