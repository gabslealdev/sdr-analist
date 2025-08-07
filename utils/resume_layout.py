
import streamlit as st
import pandas as pd

def exibir_cards_resumo(df_resumo: pd.DataFrame):
    st.subheader("📊 Resumo Comercial por Período")

    for _, row in df_resumo.iterrows():
        with st.container():
            st.markdown(f"### 🗓️ {row['PERÍODO']}")
            colunas = st.columns(6)

            colunas[0].metric("LEADS", row['LEADS'])
            colunas[1].metric("ACIONADOS", row['ACIONADOS'])
            colunas[2].metric("TRABALHADOS", row['TRABALHADOS'])
            colunas[3].metric("FALADOS", row['FALADOS'])
            colunas[4].metric("FALADOS VÁLIDOS", row['FALADOS VÁLIDOS'])
            colunas[5].metric("REUNIÕES", row['REUNIÃO AGENDADA'])