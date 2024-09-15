import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Listas de meses
meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

colunas_resultados = ['CgTR', 'CgTA', 'PHsFT', 'PHiFT', 'TOMax', 'TOMin']
colunas_entradas = ["ANG_N_ange", "ANG_N_anghd", "ANG_N_anghe", "ANG_N_angv", "ANG_O_ange",
                    "ANG_O_anghd", "ANG_O_anghe", "ANG_O_angv", "ANG_S_ange", "ANG_S_anghd",
                    "ANG_S_anghe", "ANG_S_angv", "ANG_L_ange", "ANG_L_anghd", "ANG_L_anghe",
                    "ANG_L_angv", "APP_CeilingHeight", "CONST_ThermalConductance_COB",
                    "CONST_ThermalConductance_PAR_EXT", "CONST_ThermalConductance_PISO_TERREO",
                    "CONST_cob_CT", "CONST_laje_CT", "CONST_par_ext_CT", "SAMPLE_openFactor",
                    "SAMPLE_roof_abs", "SAMPLE_shgc", "SAMPLE_uVidro", "SAMPLE_wall_abs"]


df = pd.read_csv("resultado_meses.csv")

# Seleção do mês pelo usuário
mes_selecionado = st.selectbox("Selecione o mês", meses)

# Filtrar o dataframe para o mês selecionado
df_filtrado = df[df['CLIMA_month'] == mes_selecionado]

# Calcular as médias dos resultados
resultados = ['CgTR', 'CgTA', 'PHsFT', 'PHiFT', 'TOMax', 'TOMin']
medias = {resultado: df_filtrado[resultado].mean() for resultado in resultados}

# Criar um DataFrame para a tabela
df_tabela = pd.DataFrame(list(medias.items()), columns=['Resultado', 'Média'])

# Exibir a tabela no Streamlit
st.write(f"**Médias dos Resultados para o mês de {mes_selecionado}:**")
st.dataframe(df_tabela)

# Agrupar o dataframe por 'CLIMA_month' e calcular a média dos valores
df_grouped = df.groupby('CLIMA_month').mean().reset_index()

# Função para criar o gráfico de barras interativo
def plot_interactive_bar_chart(data, coluna, meses):
    fig = px.bar(data, x='CLIMA_month', y=coluna, 
                 category_orders={'CLIMA_month': meses}, 
                 labels={'CLIMA_month': 'Mês', coluna: f'Média de {coluna}'},
                 title=f'Média de {coluna} por Mês')
    fig.update_layout(xaxis_title='Mês', yaxis_title=f'Média de {coluna}', 
                      title_x=0.5, xaxis_tickangle=-45)
    st.plotly_chart(fig)

# Lista de colunas para plotar
colunas = ['CgTR', 'CgTA', 'PHsFT', 'PHiFT', 'TOMax', 'TOMin']

# Gerar gráficos separados
for coluna in colunas:
    plot_interactive_bar_chart(df_grouped, coluna, meses)


# Selecionar apenas as colunas relevantes para o gráfico
colunas_relevantes = colunas_entradas + colunas_resultados
df_relevante = df_filtrado[colunas_relevantes]

# Criar o gráfico de coordenadas paralelas
fig = px.parallel_coordinates(df_relevante, dimensions=colunas_relevantes, color='CgTR',
                              labels={col: col for col in colunas_relevantes},
                              title=f'Gráfico de Coordenadas Paralelas para o mês de {mes_selecionado}')

# Exibir o gráfico
st.plotly_chart(fig)
    