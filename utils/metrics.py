import pandas as pd


def calcular_atingimento_diario(df, meta=30):
    hoje = pd.Timestamp.today().normalize()
    
    etapas_validas = ['FALADO', 'FALADO VÁLIDO', 'REUNIÃO AGENDADA']
    df = df[df['FUNIL DE ATENDIMENTO'].isin(etapas_validas)].copy()

    data_cols = [
        'DATA DO ACIONAMENTO I',
        'DATA DO ACIONAMENTO II',
        'DATA DO ACIONAMENTO III',
        'DATA DO ACIONAMENTO IV'
    ]

    # Cria máscara para linhas com qualquer acionamento na data de hoje
    mask = df[data_cols].apply(lambda row: hoje in row.values, axis=1)
    df_hoje = df[mask]

    # Contagem por etapa
    def contar_por_etapa(etapa):
        return df_hoje[df_hoje['FUNIL DE ATENDIMENTO'] == etapa]['SDR RESPONSÁVEL'].value_counts()

    sdrs = df_hoje['SDR RESPONSÁVEL'].dropna().unique()
    resumo = pd.DataFrame({'SDR RESPONSÁVEL': sdrs})
    resumo['FALADO'] = resumo['SDR RESPONSÁVEL'].map(contar_por_etapa('FALADO')).fillna(0).astype(int)
    resumo['FALADO VÁLIDO'] = resumo['SDR RESPONSÁVEL'].map(contar_por_etapa('FALADO VÁLIDO')).fillna(0).astype(int)
    resumo['REUNIÃO AGENDADA'] = resumo['SDR RESPONSÁVEL'].map(contar_por_etapa('REUNIÃO AGENDADA')).fillna(0).astype(int)

    # Mantém o nome original da coluna para compatibilidade
    resumo['FaladosTotais'] = resumo[['FALADO', 'FALADO VÁLIDO', 'REUNIÃO AGENDADA']].sum(axis=1)
    resumo['Meta'] = meta
    resumo['Atingimento (%)'] = (resumo['FaladosTotais'] / meta * 100).round(1)

    return resumo.sort_values(by='Atingimento (%)', ascending=False)



def calcular_reunioes_semana(df, meta=5):
    hoje = pd.Timestamp.today()
    semana_atual = hoje.isocalendar().week

    data_cols = [
        'DATA DO ACIONAMENTO I',
        'DATA DO ACIONAMENTO II',
        'DATA DO ACIONAMENTO III',
        'DATA DO ACIONAMENTO IV'
    ]

    df = df[df['FUNIL DE ATENDIMENTO'] == 'REUNIÃO AGENDADA'].copy()

    # Verifica se alguma das colunas tem a semana atual
    mask = df[data_cols].apply(
        lambda row: any(
            pd.notnull(d) and pd.Timestamp(d).isocalendar().week == semana_atual
            for d in row
        ), axis=1
    )

    df_semana = df[mask]

    resumo = (
        df_semana.groupby('SDR RESPONSÁVEL')
        .size()
        .reset_index(name='Total Reuniões')
    )

    resumo['Meta'] = meta
    resumo['Atingimento (%)'] = (resumo['Total Reuniões'] / meta * 100).round(1)

    return resumo.sort_values(by='Atingimento (%)', ascending=False)
