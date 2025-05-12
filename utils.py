import altair as alt
import streamlit as st
import pandas as pd

def plotar_casos_por_semana(df, coluna_data='DT_NOTIFIC'):
    if coluna_data not in df.columns:
        st.warning(f"Coluna '{coluna_data}' não encontrada.")
        return

    # Converte a coluna para datetime
    df[coluna_data] = pd.to_datetime(df[coluna_data], errors='coerce')

    # Remove datas inválidas
    df = df.dropna(subset=[coluna_data])

    # Cria coluna de semana epidemiológica
    df['semana_epi'] = df[coluna_data].dt.strftime('%Y-%U')  # ano-semana

    # Conta os casos por semana
    contagem = df.groupby('semana_epi').size().reset_index(name='casos')

    # Garante que o número de casos seja inteiro
    contagem['casos'] = contagem['casos'].astype(int)

    # Ordena corretamente
    contagem['semana_epi'] = pd.to_datetime(contagem['semana_epi'] + '-1', format='%Y-%U-%w')
    contagem = contagem.sort_values('semana_epi')

    # Gera o gráfico
    chart = alt.Chart(contagem).mark_bar().encode(
        x=alt.X('semana_epi:T', title='Semana Epidemiológica', axis=alt.Axis(labelAngle=-45)),  # Rotaciona os rótulos do eixo X
        y=alt.Y('casos:Q', title='Número de Casos', axis=alt.Axis(format='d')),
        color=alt.Color('casos:Q', legend=alt.Legend(title="Número de Casos", orient='right')),  # Adiciona título à legenda
        tooltip=['semana_epi:T', 'casos']
    ).properties(
        title='📈 Casos por Semana Epidemiológica',
        width=700,
        height=400
    ).configure_view(
        continuousWidth=600,
        continuousHeight=350
    )

    st.altair_chart(chart, use_container_width=True)
