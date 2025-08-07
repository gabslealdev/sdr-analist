import pandas as pd
from datetime import datetime, timedelta

# Define os valores de FUNIL por categoria
TRABALHADOS = ['TRABALHADO', 'FALADO', 'FALADO VÁLIDO', 'REUNIÃO AGENDADA']
FALADOS = ['FALADO', 'FALADO VÁLIDO', 'REUNIÃO AGENDADA']
FALADOS_VALIDOS = ['FALADO VÁLIDO', 'REUNIÃO AGENDADA']
REUNIAO_AGENDADA = 'REUNIÃO AGENDADA'

COLUNAS_ACIONAMENTO = [
    'DATA DO ACIONAMENTO I',
    'DATA DO ACIONAMENTO II',
    'DATA DO ACIONAMENTO III',
    'DATA DO ACIONAMENTO IV'
]

def preparar_colunas_data(df: pd.DataFrame) -> pd.DataFrame:
    for col in COLUNAS_ACIONAMENTO:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def filtrar_periodo(df: pd.DataFrame, periodo: str) -> pd.DataFrame:
    hoje = datetime.now().date()
    hoje_dt = pd.to_datetime(hoje)
    inicio_semana = pd.to_datetime(hoje - timedelta(days=hoje.weekday()))

    if periodo == 'hoje':
        filtro = False
        for col in COLUNAS_ACIONAMENTO:
            filtro |= df[col].dt.normalize() == hoje_dt
        return df[filtro]

    elif periodo == 'semana':
        filtro = False
        for col in COLUNAS_ACIONAMENTO:
            filtro |= df[col].dt.normalize() >= inicio_semana
        return df[filtro]

    elif periodo == 'mes':
        filtro = False
        for col in COLUNAS_ACIONAMENTO:
            filtro |= (df[col].dt.month == hoje.month) & (df[col].dt.year == hoje.year)
        return df[filtro]

    else:
        raise ValueError("Período inválido: use 'hoje', 'semana' ou 'mes'")

def calcular_linha_resumo(df_periodo: pd.DataFrame) -> dict:
    leads = len(df_periodo)
    acionados = df_periodo[COLUNAS_ACIONAMENTO].notna().any(axis=1).sum()

    trabalhados = df_periodo['FUNIL DE ATENDIMENTO'].isin(TRABALHADOS).sum()
    falados = df_periodo['FUNIL DE ATENDIMENTO'].isin(FALADOS).sum()
    falados_validos = df_periodo['FUNIL DE ATENDIMENTO'].isin(FALADOS_VALIDOS).sum()
    reunioes = (df_periodo['FUNIL DE ATENDIMENTO'] == REUNIAO_AGENDADA).sum()

    return {
        'LEADS': leads,
        'ACIONADOS': acionados,
        'TRABALHADOS': trabalhados,
        'FALADOS': falados,
        'FALADOS VÁLIDOS': falados_validos,
        'REUNIÃO AGENDADA': reunioes
    }

def gerar_resumo_geral(df: pd.DataFrame) -> pd.DataFrame:
    df = preparar_colunas_data(df)

    resumo = []

    for periodo in ['mes', 'semana', 'hoje']:
        df_filtro = filtrar_periodo(df, periodo)
        linha = calcular_linha_resumo(df_filtro)
        linha['PERÍODO'] = periodo.upper()
        resumo.append(linha)

    df_resumo = pd.DataFrame(resumo)
    df_resumo = df_resumo[['PERÍODO', 'LEADS', 'ACIONADOS', 'TRABALHADOS', 'FALADOS', 'FALADOS VÁLIDOS', 'REUNIÃO AGENDADA']]
    return df_resumo
