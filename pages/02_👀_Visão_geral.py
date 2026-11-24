import pandas as pd 
import streamlit as st  
import plotly.express as px
from utils.carrega_dados import carregar_dados,remove_outliers_iqr



st.set_page_config(
    page_title='Pagina 1',
    page_icon='📈',
    layout='wide'
)

st.title('Visão Geral')


df = carregar_dados()   

st.subheader("📊 Aprensento o Histograma das Notas por Gênero")
st.write('Movimente a barra para ajustar o número de barras no histograma.')

bins = st.slider("Número de Barras", 5, 100, 30) #numero de bins que o slide tem

fig = px.histogram(
    df,
    x="Nota_Prova",
    color="Genero",
    nbins=bins,
    barmode="overlay", 
    opacity=0.7,
    color_discrete_map={
        "Masculino": "#0529f7",     
        "Femino": "#eb07c5",   
    },
    title="Distribuição das Notas por Gênero"
)

fig.update_layout(
    xaxis_title="Nota da Prova",
    yaxis_title="Contagem",
    legend_title="Genero"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📦 Apresento o Box Plot das Atividades Extracurriculares x Notas da Prova")

st.write("""
Este gráfico compara as notas dos alunos que **participam ou não** de atividades extracurriculares.
""")

remove_outliers = st.toggle("Remover Outliers (IQR)", value=False) #remove outlier

df_plot = df.copy()

if remove_outliers:
    original_count = len(df_plot)
    df_plot = remove_outliers_iqr(df_plot, "Nota_Prova")
    removed_count = original_count - len(df_plot)
    

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Estudantes", len(df_plot))#metric mostra u card com total de estudante
with col2:
    yes_count = len(df_plot[df_plot['Atividades_Extracurriculares'] == 'Yes']) #serie booleana de True e False
    st.metric("Participam de Atividades", yes_count)
with col3:
    no_count = len(df_plot[df_plot['Atividades_Extracurriculares'] == 'No'])
    st.metric("Não Participam", no_count)


fig = px.box(
    df_plot,
    x="Atividades_Extracurriculares",
    y="Nota_Prova",
    color="Atividades_Extracurriculares",
    title="Impacto das Atividades Extracurriculares no Nota da Prova",
    color_discrete_map={
        "Sim": "#1f77b4", 
        "Não": "#d62728",   
    },
    labels={
        'Atividades_Extracurriculares': 'Atividades Extracurriculares',
        'Nota_Prova': 'Nota no Exame',}
    
)

fig.update_layout(
    xaxis_title="Participa de atividades extracurriculares?",
    yaxis_title="Nota da Prova",
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📊 Aprensento o gráfico Bar da Frequência Escolar x Nota da Prova")

st.write("""
Este gráfico mostra como o nível de **frequência escolar (Presença)** 
se relaciona com as notas finais dos alunos.
""")

df_plot = df.copy()

medias_presenca = df_plot.groupby('Presenca')['Nota_Prova'].mean()#agrupa por presença e calcula a média das notas  

fig = px.bar(
    x=medias_presenca.index,
    y=medias_presenca.values,
    color=medias_presenca.index,
    title="Nível de Presença vs. Nota da Prova",
    color_discrete_map={
        "Low": "#d62728",
        "Medium": "#ff7f0e",
        "High": "#1f77b4"
    },
    labels={'x': 'Nível de Presença', 'y': 'Nota Média da Prova'}
)

fig.update_layout(
    xaxis_title="Nível de Presença",
    yaxis_title="Nota da Prova",
    showlegend=True
)

fig.update_traces( #coloca valores as barras
    texttemplate='%{y:.1f}',
    textposition='outside'
)

st.plotly_chart(fig, use_container_width=True)







