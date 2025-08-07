import plotly.graph_objects as go
import streamlit as st

def exibir_gauge(label, nome, valor, meta, suffix="%", faixa=(0, 120), altura=150, largura=150):
    percentual = (valor / meta * 100) if meta > 0 else 0
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentual,
        delta={'reference': 100},
        title={'text': f"{label}<br><b>{nome}</b>", 'font': {'size': 14}},
        gauge={
            'axis': {'range': faixa},
            'bar': {'color': '#4a6fa5'},
            'steps': [
                {'range': [0, 50], 'color': "#ff595e"},
                {'range': [50, 90], 'color': "#ffca3a"},
                {'range': [90, faixa[1]], 'color': "#8ac926"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        },
        number={'suffix': suffix}
    ))
    
    fig.update_layout(
        height=altura,
        width=largura,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
