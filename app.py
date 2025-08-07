import streamlit as st
from datetime import datetime
from utils.loader import carregar_dados
from utils.goals import exibir_meta_diaria, exibir_meta_semanal
from utils.status import status_geral
from utils.resume import gerar_resumo_geral
from utils.resume_layout import exibir_cards_resumo


# Carrega os dados
df = carregar_dados()
if df is None:
    st.stop()

status_geral(df)
df_resumo = gerar_resumo_geral(df)
exibir_cards_resumo(df_resumo)
exibir_meta_diaria(df)
exibir_meta_semanal(df)


