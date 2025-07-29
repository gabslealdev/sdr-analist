import pandas as pd
import altair as alt
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Relatório Comercial", layout="wide")

st.title("Relatório Comercial - Persone")
 
uploaded_file = st.file_uploader("Faça o upload da base que está trabalhando", type=["xlsx"])

if not uploaded_file:
    st.info("Por favor, envie um arquivo para começar.")
    st.stop()

df = pd.read_excel(uploaded_file)
df.columns = df.columns.str.strip()

# lista todas as colunas do tipo data
data_cols = [
    'DATA DO ACIONAMENTO I',
    'DATA DO ACIONAMENTO II',
    'DATA DO ACIONAMENTO III',
    'DATA DO ACIONAMENTO IV'
]

# Conversão para datetime
for col in data_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')
    
# Colunas obrigatórias    
mailing_cols = [
    'ID','ORIGEM', 'CÓDIGO DA INSTITUIÇÃO', 'EMPRESA', 'TELEFONE DA INSTITUIÇÃO', 
    'DATA DO ACIONAMENTO I', 'DATA DO ACIONAMENTO II', 'DATA DO ACIONAMENTO III',
    'DATA DO ACIONAMENTO IV', 'FUNIL DE ATENDIMENTO', 'FUNIL DE VENDA' 'TABULAÇÃO N1', 'TABULAÇÃO N2',
    'TABULAÇÃO N3',    'OBSERVAÇÕES','CONTATO I', 'ÁREA I', 'EMAIL I',
    'TELEFONE CONTATO I', 'CONTATO II', 'ÁREA II', 'EMAIL II',
    'TELEFONE CONTATO II', 'CONTATO III', 'ÁREA III', 'EMAIL III',
    'TELEFONE CONTATO III','SIGLA',
    'TIPO DE EMPRESA', 'DEPENDÊNCIA ADMINISTRATIVA', 'CATEGORIA',
    'GRUPO CONSOLIDADOR', 'NÍVEL DE ENSINO', 'RANGE DE MATRÍCULAS',
    'TOTAL DE MATRÍCULAS', 'TICKET MÉDIO', 'ENDEREÇO', 'NÚMERO',
    'COMPLEMENTO', 'BAIRRO', 'CEP', 'MUNICÍPIO', 'ESTADO', 'REGIÃO', 'SDR RESPONSÁVEL'
]

# Filtro por SDR
sdrs = df['SDR RESPONSÁVEL'].dropna().unique()
sdr = st.sidebar.multiselect("Filtrar por SDR", sdrs)
df = df[df['SDR RESPONSÁVEL'].isin(sdr)] if sdr else df

# Função de métricas
def calcular_metricas(df_):
    total = len(df_)
    acionados = df_['DATA DO ACIONAMENTO I'].notna().sum()
    cobertura = (acionados / total * 100) if total > 0 else 0
    trabalhados = df_[df_['FUNIL DE ATENDIMENTO'].str.upper() != 'LEAD' ].shape[0]
    falados = df_[df_['FUNIL DE ATENDIMENTO'].isin(['FALADO'])].shape[0]
    falados_validos = df_[df_['FUNIL DE ATENDIMENTO'].isin(['FALADO VÁLIDO'])].shape[0]
    agendamentos = df_[df_['FUNIL DE ATENDIMENTO'].isin(['REUNIÃO AGENDADA'])].shape[0]
    return total, acionados, cobertura, trabalhados, falados, falados_validos, agendamentos

# Status Geral
st.subheader("Status Geral da Base")
total, acionados, cobertura, *_ = calcular_metricas(df)
col1, col2, col3 = st.columns(3)
col1.metric("LEADS", total)
col2.metric("ACIONADOS", acionados)
col3.metric("COBERTURA", f"{cobertura:.1f}%") 

# Filtros por tempo
today = pd.to_datetime(datetime.now().date())
df_mes = df[df['DATA DO ACIONAMENTO I'].dt.month == today.month]
df_semana = df[df['DATA DO ACIONAMENTO I'].dt.isocalendar().week == today.isocalendar().week]
df_hoje = df[df['DATA DO ACIONAMENTO I'].dt.date == today.date()] 

# Métricas por período
for label, dfx in {
    "📅 Este Mês": df_mes,
    "📆 Esta Semana": df_semana,
    "📍 Hoje": df_hoje
}.items():
    st.subheader(label)
    total, acionados, cobertura, trabalhados, falados, falados_validos, agendamentos = calcular_metricas(dfx)
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("LEADS", total)
    col2.metric("ACIONADOS", acionados)
    col3.metric("COBERTURA", f"{cobertura:.1f}%")
    col4.metric("TRABALHADOS", trabalhados)
    col5.metric("FALADOS", falados)
    col6.metric("FALADOS VÁLIDOS", falados_validos)
    col7.metric("REUNIÃO AGENDADA", agendamentos)
    
# Funil de Vendas
if 'FUNIL DE ATENDIMENTO' in df.columns:
    st.subheader("🚀 Funil de Vendas Geral")

    funil_df = (
        df['FUNIL DE ATENDIMENTO']
        .value_counts()
        .reset_index()
    )

    chart = alt.Chart(funil_df).mark_bar().encode(
        x=alt.X('Quantidade:Q', title='Leads'),
        y=alt.Y('Etapa:N', sort='-x', title='Etapas'),
        color='Etapa:N'
    ).properties(width=700, height=300)

    st.altair_chart(chart)

# Tabela opcional
st.subheader("Ver os dados do mailing")
if st.toggle("Mostrar tabela com todos os dados filtrados"):
    st.dataframe(df)