import pandas as pd
import streamlit as st

def carregar_dados():
    st.set_page_config(page_title="Relatório Comercial", layout="wide")
    st.title("Relatório Comercial - Persone")
    
    uploaded_file = st.file_uploader("Faça o upload da base que está trabalhando", type=["xlsx"])
    if not uploaded_file:
        st.info("Por favor, envie um arquivo para começar.")
        return None
    
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    
    data_cols = [
        'DATA DO ACIONAMENTO I', 'DATA DO ACIONAMENTO II',
        'DATA DO ACIONAMENTO III', 'DATA DO ACIONAMENTO IV'
    ]
    for col in data_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df        
    