import streamlit as st
import pandas as pd
from utils.gauge import exibir_gauge
from utils.metrics import calcular_atingimento_diario, calcular_reunioes_semana



def exibir_meta_diaria(df: pd.DataFrame, meta: int = 15):
    resumo_dia = calcular_atingimento_diario(df, meta)
    st.subheader("\U0001F4DE Meta Diária de Acionamentos")

    if not resumo_dia.empty:
        for i in range(0, len(resumo_dia), 2):
            cols = st.columns(2)
            for col, (_, row) in zip(cols, resumo_dia.iloc[i:i + 2].iterrows()):
                with col:
                    exibir_gauge(
                        "Meta Diária",
                        row['SDR RESPONSÁVEL'],
                        row['FaladosTotais'],
                        meta,
                        altura=200,
                        largura=200
                    )
                    st.markdown(f"**\U0001F4DE {row['FaladosTotais']} falados no total**")
    else:
        st.info("Nenhum acionamento registrado hoje.")


def exibir_meta_semanal(df: pd.DataFrame, meta: int = 5):
    resumo_semana = calcular_reunioes_semana(df, meta)
    st.subheader("\U0001F4C5 Meta Semanal de Reuniões Agendadas")

    if not resumo_semana.empty:
        for i in range(0, len(resumo_semana), 2):
            cols = st.columns(2)
            for col, (_, row) in zip(cols, resumo_semana.iloc[i:i + 2].iterrows()):
                with col:
                    exibir_gauge(
                        "Meta Semanal",
                        row['SDR RESPONSÁVEL'],
                        row['Total Reuniões'],
                        meta,
                        altura=200,
                        largura=200
                    )
                    st.markdown(f"**\U0001F4C5 {row['Total Reuniões']} reuniões agendadas**")
    else:
        st.info("Nenhuma reunião agendada nesta semana.")
