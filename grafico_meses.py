import streamlit as st
import pandas as pd
import plotly.express as px

# Listas de meses
meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

colunas_resultados = ['CgTR', 'CgTA', 'PHsFT', 'PHiFT', 'TOMax', 'TOMin']

df_natal = pd.read_csv("resultado_meses_natal.csv")
df_caico = pd.read_csv("resultado_meses_caico.csv")

# Seleção do mês e da cidade pelo usuário
mes_selecionado = st.sidebar.selectbox("Selecione o mês", meses)
cidade_selecionada = st.selectbox("Selecione a cidade", ["Natal", "Caicó"])

if cidade_selecionada == "Natal":
    df = df_natal
else:
    df = df_caico

# Converter 'CLIMA_month' em categoria ordenada para manter a sequência correta
df['CLIMA_month'] = pd.Categorical(df['CLIMA_month'], categories=meses, ordered=True)

# Filtrar o dataframe para o mês selecionado
df_filtrado = df[df['CLIMA_month'] == mes_selecionado]

# Exibir a tabela no Streamlit
st.sidebar.write(f"**Médias dos Resultados para o mês de {mes_selecionado}:**")
st.sidebar.dataframe(df_filtrado[['CgTR', 'CgTA', 'PHsFT', 'PHiFT', 'TOMax', 'TOMin']].describe())

# Agrupar o dataframe por 'CLIMA_month' e calcular o máximo e a média dos valores
df_grouped_max = df.groupby('CLIMA_month').max().reset_index()
df_grouped_mean = df.groupby('CLIMA_month').mean().reset_index()

# Função para criar o gráfico de barras interativo com linha da média
def plot_interactive_bar_chart(data_max, data_mean, coluna, meses):
    fig = px.bar(data_max, x='CLIMA_month', y=coluna, 
                 category_orders={'CLIMA_month': meses}, 
                 labels={'CLIMA_month': 'Mês', coluna: f'Máximo de {coluna}'},
                 title=f'Máximo de {coluna} por Mês')
    
    # Adicionar linha da média
    fig.add_scatter(x=data_mean['CLIMA_month'], y=data_mean[coluna], 
                    mode='lines+markers', name=f'Média de {coluna}', line=dict(color='red'))
    
    fig.update_layout(xaxis_title='Mês', yaxis_title=f'Máximo de {coluna}', 
                      title_x=0.5, xaxis_tickangle=-45)
    return fig

# Função para criar o boxplot
def plot_boxplot(data, coluna, meses):
    fig = px.box(data, x='CLIMA_month', y=coluna, 
                 category_orders={'CLIMA_month': meses},
                 labels={'CLIMA_month': 'Mês', coluna: f'Distribuição de {coluna}'},
                 title=f'Boxplot de {coluna} por Mês')
    fig.update_layout(xaxis_title='Mês', yaxis_title=f'{coluna}', title_x=0.5)
    return fig

# Gerar tabs para cada coluna de resultados
for coluna in colunas_resultados:
    tab1, tab2 = st.tabs([f"Gráfico de Barras - {coluna}", f"Boxplot - {coluna}"])
    
    with tab1:
        st.plotly_chart(plot_interactive_bar_chart(df_grouped_max, df_grouped_mean, coluna, meses))
    
    with tab2:
        st.plotly_chart(plot_boxplot(df, coluna, meses))
