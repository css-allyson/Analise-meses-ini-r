import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Listas de meses
meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

# Colunas de resultados
colunas_resultados = ['CgTR', 'CgTA', 'PHsFT', 'PHiFT', 'TOMax', 'TOMin']

# Carregar os dataframes de Natal e Caicó
df_natal = pd.read_csv("resultado_meses_natal.csv")
df_caico = pd.read_csv("resultado_meses_caico.csv")

# Seleção do mês e cidade pelo usuário
mes_selecionado = st.sidebar.selectbox("Selecione o mês", meses)
cidade_selecionada = st.selectbox("Selecione a cidade", ["Natal", "Caicó"])

# Filtrar o dataframe pela cidade selecionada
if cidade_selecionada == "Natal":
    df = df_natal
else:
    df = df_caico

# Filtrar o dataframe para o mês selecionado
df_filtrado = df[df['CLIMA_month'] == mes_selecionado]

# Exibir a tabela no Streamlit
st.sidebar.write(f"**Estatísticas descritivas para o mês de {mes_selecionado}:**")
st.sidebar.dataframe(df_filtrado[colunas_resultados].describe())

# Agrupar o dataframe por 'CLIMA_month' e calcular o valor máximo e a média dos resultados
df_grouped_max = df.groupby('CLIMA_month').max().reset_index()
df_grouped_mean = df.groupby('CLIMA_month').mean().reset_index()

# Converter 'CLIMA_month' para uma categoria ordenada com base na lista 'meses'
df_grouped_max['CLIMA_month'] = pd.Categorical(df_grouped_max['CLIMA_month'], categories=meses, ordered=True)
df_grouped_mean['CLIMA_month'] = pd.Categorical(df_grouped_mean['CLIMA_month'], categories=meses, ordered=True)

# Reordenar os dataframes de acordo com a ordem dos meses
df_grouped_max = df_grouped_max.sort_values('CLIMA_month')
df_grouped_mean = df_grouped_mean.sort_values('CLIMA_month')

# Função para criar o gráfico de barras interativo com linha de média
def plot_interactive_bar_chart_with_mean(data_max, data_mean, coluna, meses):
    # Gráfico de barras com o valor máximo
    fig_bar = px.bar(data_max, x='CLIMA_month', y=coluna, 
                     category_orders={'CLIMA_month': meses}, 
                     labels={'CLIMA_month': 'Mês', coluna: f'Valor Máximo de {coluna}'},
                     title=f'Valor Máximo de {coluna} por Mês')
    
    # Adicionar linha da média dos meses
    fig_bar.add_trace(go.Scatter(
        x=data_mean['CLIMA_month'], 
        y=data_mean[coluna],
        mode='lines+markers',
        name='Média',
        line=dict(color='red', dash='dash')
    ))
    
    # Ajustes no layout do gráfico de barras
    fig_bar.update_layout(xaxis_title='Mês', yaxis_title=f'Valor Máximo de {coluna}', 
                          title_x=0.5, xaxis_tickangle=-45)
    
    return fig_bar

# Função para criar o boxplot
def plot_boxplot(data, coluna):
    # Gráfico boxplot para a coluna selecionada
    fig_box = px.box(data, x='CLIMA_month', y=coluna, 
                     category_orders={'CLIMA_month': meses},
                     labels={'CLIMA_month': 'Mês', coluna: f'Boxplot de {coluna}'},
                     title=f'Boxplot de {coluna} por Mês')
    fig_box.update_layout(xaxis_title='Mês', yaxis_title=f'{coluna}', title_x=0.5)
    
    return fig_box

# Gerar gráficos separados para cada coluna de resultados
for coluna in colunas_resultados:
    # Dividir a área em duas colunas com proporções diferentes: 70% para o gráfico de barras e 30% para o boxplot
    col1, col2 = st.columns([0.7, 0.3])
    
    # Gráfico de barras com linha de média
    with col1:
        st.plotly_chart(plot_interactive_bar_chart_with_mean(df_grouped_max, df_grouped_mean, coluna, meses))
    
    # Gráfico boxplot
    with col2:
        st.plotly_chart(plot_boxplot(df, coluna))
