import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.subplots as psub

st.set_page_config(
    page_title="Desempenho Educacional",
    layout="wide",
    page_icon="✨"
)

st.markdown(""" <style>
footer {visibility: hidden;}
h1 {text-align: center;}
</style> """, unsafe_allow_html=True)

st.markdown(f""" <style>
    .appview-container .main .block-container{{
        padding-top: {0}rem;
        padding-right: {1.5}rem;
        padding-left: {1.5}rem;
        padding-bottom: {0}rem;
    }} </style> """, unsafe_allow_html=True)

st.markdown(f"""
<style>
div[data-testid="stMetric"] {{
  padding-top: {0}rem;
        padding-right: {5}rem;
        padding-left: {5}rem;
        padding-bottom: {0}rem;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
div[data-testid="column"] {{
  text-align: center;
}}
</style>
""", unsafe_allow_html=True)

st.title('Análise de Desempenho Educacional - 2020-2022')
st.divider()

df = pd.read_csv('./PEDE_PASSOS_DATASET_FIAP.csv', delimiter=';')

# Separando as colunas do dataframe por ano
df_2020 = df[['NOME'] + [col for col in df.columns if '2020' in col]]
df_2021 = df[['NOME'] + [col for col in df.columns if '2021' in col]]
df_2022 = df[['NOME'] + [col for col in df.columns if '2022' in col]]

# Removendo as linhas que têm somente valor na coluna "NOME" e o restante NaN
df_2020.dropna(how='all', subset=df_2020.columns.difference(['NOME']), inplace=True)
df_2021.dropna(how='all', subset=df_2021.columns.difference(['NOME']), inplace=True)
df_2022.dropna(how='all', subset=df_2022.columns.difference(['NOME']), inplace=True)

# Removendo a linha do aluno ALUNO-1259 no dataset de 2020 por conter dados inconsistentes
df_2020 = df_2020[df_2020['NOME'] != 'ALUNO-1259']

# Para a coluna PONTO_VIRADA_2020, substituir NaN por "Não"
df_2020['PONTO_VIRADA_2020'].fillna("Não", inplace=True)

# Para a coluna DESTAQUE_IPV_2020, substituir NaN por ""
df_2020['DESTAQUE_IPV_2020'].fillna("Sem Destaque", inplace=True)

# Dataset 2020: Tipagem adequada para cada coluna
df_2020 = df_2020.astype({
    'IDADE_ALUNO_2020': 'int64',
    'ANOS_PM_2020': 'int64',
    'INDE_2020': 'float64',
    'IAA_2020': 'float64',
    'IEG_2020': 'float64',
    'IPS_2020': 'float64',
    'IDA_2020': 'float64',
    'IPP_2020': 'float64',
    'IPV_2020': 'float64',
    'IAN_2020': 'float64'
})


df_2021['PEDRA_2021'].replace('#NULO!', '', inplace=True)
df_2021['INDE_2021'].replace('#NULO!', 0, inplace=True)
df_2021['PONTO_VIRADA_2021'].replace('#NULO!', 'Não', inplace=True)


df_2021 = df_2021.astype({
'FASE_2021':'int64',
'TURMA_2021':'object',
'INSTITUICAO_ENSINO_ALUNO_2021':'object',
'SINALIZADOR_INGRESSANTE_2021':'object',
'PEDRA_2021':'object',
'INDE_2021':'float64',
'IAA_2021':'float64',
'IEG_2021':'float64',
'IPS_2021':'float64',
'IDA_2021':'float64',
'IPP_2021':'float64',
'REC_EQUIPE_1_2021':'object',
'REC_EQUIPE_2_2021':'object',
'REC_EQUIPE_3_2021':'object',
'REC_EQUIPE_4_2021':'object',
'PONTO_VIRADA_2021':'object',
'IPV_2021':'float64',
'IAN_2021':'float64',
'NIVEL_IDEAL_2021':'object',
'DEFASAGEM_2021':'int64',
})

# Substituindo NaN por 0 nas colunas de notas
df_2022['NOTA_PORT_2022'].fillna(0, inplace=True)
df_2022['NOTA_MAT_2022'].fillna(0, inplace=True)
df_2022['NOTA_ING_2022'].fillna(0, inplace=True)

# Substituindo NaN nas colunas de recuperação
df_2022['REC_AVA_3_2022'].fillna('Sem Ava', inplace=True)
df_2022['REC_AVA_4_2022'].fillna('Sem Ava', inplace=True)

df_2022_final = df_2022.astype({
    'FASE_2022': 'int64',
    'ANO_INGRESSO_2022': 'int64',
    'INDE_2022': 'float64',
    'CG_2022': 'float64',
    'CF_2022': 'float64',
    'CT_2022': 'float64',
    'IAA_2022': 'float64',
    'IEG_2022': 'float64',
    'IPS_2022': 'float64',
    'IDA_2022': 'float64',
    'NOTA_PORT_2022': 'float64',
    'NOTA_MAT_2022': 'float64',
    'NOTA_ING_2022': 'float64',
    'QTD_AVAL_2022': 'int64',
    'IPP_2022': 'float64',
    'IPV_2022': 'float64',
    'IAN_2022': 'float64'
})

def rename_columns(df, year):
    return df.rename(columns=lambda x: x.replace(f'_{year}', ''))

df_2020 = rename_columns(df_2020, '2020')
df_2021 = rename_columns(df_2021, '2021')
df_2022 = rename_columns(df_2022, '2022')


# normalizando FASE_TURMA de 2020 para ficar igual a 2021 e 2022
df_2020['FASE'] = df_2020['FASE_TURMA'].str[0]
df_2020['TURMA'] = df_2020['FASE_TURMA'].str[1]
df_2020.drop(columns=['FASE_TURMA'], inplace=True)
df_2020['FASE'] = df_2020['FASE'].astype('int64')

# Criando a nova coluna SINALIZADOR_INGRESSANTE com base na condição ANOS_PM
df_2020['SINALIZADOR_INGRESSANTE'] = df_2020['ANOS_PM'].apply(lambda x: 'Veterano' if x > 0 else 'Ingressante')
df_2020.drop(columns=['ANOS_PM'], inplace=True)

# Alterando os valores na coluna INSTITUICAO_ENSINO_ALUNO
df_2020['INSTITUICAO_ENSINO_ALUNO'] = df_2020['INSTITUICAO_ENSINO_ALUNO'].apply(
    lambda x: 'Escola Pública' if x == 'Escola Pública' else 'Escola Particular'
)

# Criando a nova coluna BOLSA com base na INSTITUICAO_ENSINO_ALUNO
df_2020['BOLSA'] = df_2020['INSTITUICAO_ENSINO_ALUNO'].apply(
    lambda x: 'Sim' if x == 'Escola Particular' else 'Não'
)

# dropar as colunas que não tem mais utilidade
df_2020.drop(columns=['DESTAQUE_IEG', 'INDE_CONCEITO', 'DESTAQUE_IDA', 'DESTAQUE_IPV','IDADE_ALUNO'], inplace=True)

# Alterando os valores na coluna INSTITUICAO_ENSINO_ALUNO
df_2021['INSTITUICAO_ENSINO_ALUNO'] = df_2021['INSTITUICAO_ENSINO_ALUNO'].apply(
    lambda x: 'Escola Pública' if x == 'Escola Pública' else 'Escola Particular'
)

# Criando a nova coluna BOLSA com base na INSTITUICAO_ENSINO_ALUNO
df_2021['BOLSA'] = df_2021['INSTITUICAO_ENSINO_ALUNO'].apply(
    lambda x: 'Sim' if x == 'Escola Particular' else 'Não'
)

df_2021.drop(columns=['REC_EQUIPE_1', 'REC_EQUIPE_2', 'REC_EQUIPE_3', 'REC_EQUIPE_4', 'NIVEL_IDEAL', 'DEFASAGEM'], inplace=True)

# Criando a nova coluna SINALIZADOR_INGRESSANTE com base na condição ANO_INGRESSO
df_2022['SINALIZADOR_INGRESSANTE'] = df_2022['ANO_INGRESSO'].apply(lambda x: 'Veterano' if x < 2022 else 'Ingressante')
df_2022.drop(columns=['ANO_INGRESSO'], inplace=True)

# Criando a nova coluna INSTITUICAO_ENSINO_ALUNO com base na BOLSISTA
df_2022['INSTITUICAO_ENSINO_ALUNO'] = df_2022['BOLSISTA'].apply(
    lambda x: 'Escola Particular' if x == 'Sim' else 'Escola Pública'
)

# renomear a coluna BOLSISTA para BOLSA
df_2022.rename(columns={'BOLSISTA': 'BOLSA'}, inplace=True)

#dropar as colunas que não tem mais utilidade
df_2022.drop(columns=['NOTA_PORT', 'NOTA_MAT', 'NOTA_ING', 'QTD_AVAL', 'REC_AVA_1', 'REC_AVA_2', 'REC_AVA_3', 
                      'REC_AVA_4', 'INDICADO_BOLSA', 'NIVEL_IDEAL','CF', 'CG', 'CT', 'DESTAQUE_IDA', 'DESTAQUE_IEG', 'DESTAQUE_IPV'], inplace=True)


# Contagem de alunos e variação percentual
total_alunos_2020 = df_2020['NOME'].nunique()
total_alunos_2021 = df_2021['NOME'].nunique()
total_alunos_2022 = df_2022['NOME'].nunique()

anos = ['2020', '2021', '2022']
total_alunos = [total_alunos_2020, total_alunos_2021, total_alunos_2022]

variacao_percentual = [0]
variacao_percentual.append(((total_alunos_2021 - total_alunos_2020) / total_alunos_2020) * 100)
variacao_percentual.append(((total_alunos_2022 - total_alunos_2021) / total_alunos_2021) * 100)

fig_ano = go.Figure()
fig_ano.add_trace(go.Bar(
    x=anos,
    y=total_alunos,
    text=[f'{v:.2f}%' for v in variacao_percentual],
    textposition='inside',
    name='Total de Alunos'
))
fig_ano.update_layout(
    title='Total de Alunos com Variação Percentual',
    xaxis_title='Ano',
    yaxis_title='Total de Alunos',
    showlegend=False
)

# Gráfico 2: Distribuição de Ingressantes e Veteranos por Ano

ingressantes_2020 = df_2020[df_2020['SINALIZADOR_INGRESSANTE'] == 'Ingressante'].shape[0]
veteranos_2020 = df_2020[df_2020['SINALIZADOR_INGRESSANTE'] == 'Veterano'].shape[0]

ingressantes_2021 = df_2021[df_2021['SINALIZADOR_INGRESSANTE'] == 'Ingressante'].shape[0]
veteranos_2021 = df_2021[df_2021['SINALIZADOR_INGRESSANTE'] == 'Veterano'].shape[0]

ingressantes_2022 = df_2022[df_2022['SINALIZADOR_INGRESSANTE'] == 'Ingressante'].shape[0]
veteranos_2022 = df_2022[df_2022['SINALIZADOR_INGRESSANTE'] == 'Veterano'].shape[0]

anos = ['2020', '2021', '2022']
ingressantes = [ingressantes_2020, ingressantes_2021, ingressantes_2022]
veteranos = [veteranos_2020, veteranos_2021, veteranos_2022]

fig_iv = go.Figure(data=[
    go.Bar(name='Ingressantes', x=anos, y=ingressantes),
    go.Bar(name='Veteranos', x=anos, y=veteranos)
])

fig_iv.update_layout(
    barmode='stack',
    title='Distribuição de Ingressantes e Veteranos',
    xaxis_title='Ano',
    yaxis_title='Número de Alunos',
    legend_title='Categoria'
)


# Criando duas colunas para exibir os gráficos lado a lado
col1, col2 = st.columns(2)

# Exibindo o primeiro gráfico na primeira coluna
with col1:
    st.plotly_chart(fig_ano)

# Exibindo o segundo gráfico na segunda coluna
with col2:
    st.plotly_chart(fig_iv)

st.divider()
# Gráfico 4: Distribuição de Alunos em Escolas Públicas vs Particulares (2020-2022)

# Contando o número de alunos de escolas públicas e particulares para cada ano
publicos_2020 = df_2020[df_2020['INSTITUICAO_ENSINO_ALUNO'] == 'Escola Pública']['NOME'].nunique()
particulares_2020 = df_2020[df_2020['INSTITUICAO_ENSINO_ALUNO'] == 'Escola Particular']['NOME'].nunique()

publicos_2021 = df_2021[df_2021['INSTITUICAO_ENSINO_ALUNO'] == 'Escola Pública']['NOME'].nunique()
particulares_2021 = df_2021[df_2021['INSTITUICAO_ENSINO_ALUNO'] == 'Escola Particular']['NOME'].nunique()

publicos_2022 = df_2022[df_2022['INSTITUICAO_ENSINO_ALUNO'] == 'Escola Pública']['NOME'].nunique()
particulares_2022 = df_2022[df_2022['INSTITUICAO_ENSINO_ALUNO'] == 'Escola Particular']['NOME'].nunique()

# Organizando os dados
categorias = ['Escola Pública', 'Escola Particular']
valores_2020 = [publicos_2020, particulares_2020]
valores_2021 = [publicos_2021, particulares_2021]
valores_2022 = [publicos_2022, particulares_2022]

# Criando o subplot para 3 gráficos de pizza
fig_p = psub.make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                         subplot_titles=['2020', '2021', '2022'])

# Adicionando o gráfico de pizza para 2020
fig_p.add_trace(go.Pie(labels=categorias, values=valores_2020, name='2020'), 1, 1)

# Adicionando o gráfico de pizza para 2021
fig_p.add_trace(go.Pie(labels=categorias, values=valores_2021, name='2021'), 1, 2)

# Adicionando o gráfico de pizza para 2022
fig_p.add_trace(go.Pie(labels=categorias, values=valores_2022, name='2022'), 1, 3)

# Configurando o layout do gráfico
fig_p.update_layout(
    title_text='Distribuição de Alunos em Escolas Públicas vs Particulares',
)

# Exibindo o gráfico
st.plotly_chart(fig_p)

st.divider()
# Gráfico 3: Ingressantes vs Evadidos por Ano

# Primeiro, vamos criar sets dos alunos de cada ano
alunos_2020 = set(df_2020['NOME'])
alunos_2021 = set(df_2021['NOME'])
alunos_2022 = set(df_2022['NOME'])

# Alunos que estavam em 2020 e sumiram em 2021 ou 2022
desistentes_2020 = alunos_2020 - (alunos_2021 | alunos_2022)

# Alunos que estavam em 2021 e sumiram em 2022
desistentes_2021 = alunos_2021 - alunos_2022

# Total de desistentes por ano
total_desistentes_2020 = len(desistentes_2020)
total_desistentes_2021 = len(desistentes_2021)

ingressantes_2020 = df_2020[df_2020['SINALIZADOR_INGRESSANTE'] == 'Ingressante'].shape[0]
ingressantes_2021 = df_2021[df_2021['SINALIZADOR_INGRESSANTE'] == 'Ingressante'].shape[0]

# Dados
anos = ['2020', '2021']
ingressantes = [ingressantes_2020, ingressantes_2021]
evadidos = [total_desistentes_2020, total_desistentes_2021]

# Criando o gráfico de linhas
fig_ie = go.Figure()

# Linha para ingressantes com os valores em cima das linhas
fig_ie.add_trace(go.Scatter(
    x=anos,
    y=ingressantes,
    mode='lines+markers+text',
    name='Ingressantes',
    line=dict(color='green', width=4),
    text=ingressantes,
    textposition='top center'
))

# Linha para evadidos com os valores em cima das linhas
fig_ie.add_trace(go.Scatter(
    x=anos,
    y=evadidos,
    mode='lines+markers+text',
    name='Evadidos',
    line=dict(color='red', width=4),
    text=evadidos,
    textposition='top center'
))

# Configurando o layout do gráfico
fig_ie.update_layout(
    title='Ingressantes vs Evadidos por Ano',
    xaxis_title='Ano',
    yaxis_title='Número de Alunos',
    showlegend=True
)

# Gráfico 5: Distribuição de Bolsistas por Ano

# Identificando alunos que não tinham bolsa em 2020 e ganharam em 2021
sem_bolsa_2020 = df_2020[df_2020['BOLSA'] == 'Não']['NOME']
com_bolsa_2021 = df_2021[(df_2021['BOLSA'] == 'Sim') & (df_2021['NOME'].isin(sem_bolsa_2020))]

alunos_ganharam_bolsa_2021 = com_bolsa_2021['NOME'].nunique()

# Identificando alunos que não tinham bolsa em 2021 e ganharam em 2022
sem_bolsa_2021 = df_2021[df_2021['BOLSA'] == 'Não']['NOME']
com_bolsa_2022 = df_2022[(df_2022['BOLSA'] == 'Sim') & (df_2022['NOME'].isin(sem_bolsa_2021))]

alunos_ganharam_bolsa_2022 = com_bolsa_2022['NOME'].nunique()

# Criando um DataFrame com os dados
data = {
    'Ano': ['2021', '2022'],
    'Alunos que Ganharam Bolsa': [alunos_ganharam_bolsa_2021, alunos_ganharam_bolsa_2022]
}

df_bolsa= pd.DataFrame(data)

# Criando o gráfico de colunas agrupadas
fig_bo = px.bar(df_bolsa, x='Ano', y='Alunos que Ganharam Bolsa', 
             text='Alunos que Ganharam Bolsa', 
             title='Número de Alunos que Ganharam Bolsa de Um Ano para o Outro',
             labels={'Alunos que Ganharam Bolsa': 'Quantidade de Alunos'})

# Customizando o layout
fig_bo.update_traces(textposition='inside')
fig_bo.update_layout(showlegend=False)

# Criando duas colunas para exibir os gráficos lado a lado
col1, col2 = st.columns(2)

# Exibindo o primeiro gráfico na primeira coluna
with col1:
    st.plotly_chart(fig_ie)

# Exibindo o segundo gráfico na segunda coluna
with col2:
    st.plotly_chart(fig_bo)


st.divider()
# Gráfico 6: Distribuição de Alunos por Fase e Ano

# Contando a quantidade de alunos por fase para cada ano
fase_por_ano_2020 = df_2020.groupby('FASE')['NOME'].count().reset_index()
fase_por_ano_2020['Ano'] = 2020

fase_por_ano_2021 = df_2021.groupby('FASE')['NOME'].count().reset_index()
fase_por_ano_2021['Ano'] = 2021

fase_por_ano_2022 = df_2022.groupby('FASE')['NOME'].count().reset_index()
fase_por_ano_2022['Ano'] = 2022

# Concatenando os resultados em um único DataFrame
fase_por_ano = pd.concat([fase_por_ano_2020, fase_por_ano_2021, fase_por_ano_2022])

fase_por_ano.columns = ['Fase', 'Quantidade de Alunos', 'Ano']

# Criando o gráfico de barras empilhadas
fig_f = px.bar(fase_por_ano, x='Ano', y='Quantidade de Alunos', color='Fase',
             text='Quantidade de Alunos', 
             title='Distribuição de Alunos por Fase',
             labels={'Quantidade de Alunos': 'Quantidade', 'Ano': 'Ano', 'Fase': 'Fase'})

# Customizando o layout
fig_f.update_traces(textposition='inside', textfont_size=12)
fig_f.update_layout(barmode='stack')


# Exibindo o gráfico
st.plotly_chart(fig_f)

st.divider()
# Gráfico 8: Distribuição Percentual de Alunos por Pedra

# Contando a quantidade de alunos por pedra para cada ano
pedra_por_ano_2020 = df_2020.groupby('PEDRA')['NOME'].count().reset_index()
pedra_por_ano_2020['Ano'] = 2020

pedra_por_ano_2021 = df_2021.groupby('PEDRA')['NOME'].count().reset_index()
pedra_por_ano_2021['Ano'] = 2021

pedra_por_ano_2022 = df_2022.groupby('PEDRA')['NOME'].count().reset_index()
pedra_por_ano_2022['Ano'] = 2022

# Adicionando a coluna de porcentagem para cada ano
pedra_por_ano_2020['Percentual'] = (pedra_por_ano_2020['NOME'] / pedra_por_ano_2020['NOME'].sum()) * 100
pedra_por_ano_2021['Percentual'] = (pedra_por_ano_2021['NOME'] / pedra_por_ano_2021['NOME'].sum()) * 100
pedra_por_ano_2022['Percentual'] = (pedra_por_ano_2022['NOME'] / pedra_por_ano_2022['NOME'].sum()) * 100

# Concatenando os resultados em um único DataFrame
pedra_por_ano = pd.concat([pedra_por_ano_2020, pedra_por_ano_2021, pedra_por_ano_2022])

# Ajustando os nomes das colunas
pedra_por_ano.columns = ['Pedra', 'Quantidade de Alunos', 'Ano', 'Percentual']

# Arredondando o percentual para 2 casas decimais
pedra_por_ano['Percentual'] = pedra_por_ano['Percentual'].round(2)

# Criando um dicionário para associar as pedras ao intervalo de valores
valor_pedra = {
    'Quartzo': 1,
    'Ágata': 2,
    'Ametista': 3,
    'Topázio': 4
}

# Adicionando a coluna de ordem com base no intervalo de valores
pedra_por_ano['Ordem'] = pedra_por_ano['Pedra'].map(valor_pedra)

# Ordenando o DataFrame com base na coluna 'Ordem'
pedra_por_ano = pedra_por_ano.sort_values(by='Ordem')

# Criando o gráfico de barras empilhadas com percentuais e ordenado
fig_pe = px.bar(pedra_por_ano, x='Ano', y='Percentual', color='Pedra',
             text=pedra_por_ano['Percentual'].apply(lambda x: f'{x:.2f}%'), 
             title='Distribuição Percentual de Alunos por Pedra',
             labels={'Percentual': 'Percentual (%)', 'Ano': 'Ano', 'Pedra': 'Tipo de Pedra'})

# Customizando o layout
fig_pe.update_traces(textposition='inside', textfont_size=12)
fig_pe.update_layout(barmode='stack')

# Exibindo o gráfico
st.plotly_chart(fig_pe)

st.divider()
# Gráfico 9: Perfil Médio dos Índices

indices = ['IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN', 'INDE']
# Criando os dados para cada ano
radar_data_2020 = df_2020[indices].mean().reset_index()
radar_data_2020.columns = ['Indicador', 'Média']

radar_data_2021 = df_2021[indices].mean().reset_index()
radar_data_2021.columns = ['Indicador', 'Média']

radar_data_2022 = df_2022[indices].mean().reset_index()
radar_data_2022.columns = ['Indicador', 'Média']

# Criando subplots sem títulos individuais para cada gráfico
fig_m = psub.make_subplots(rows=1, cols=3, 
                         specs=[[{'type': 'polar'}, {'type': 'polar'}, {'type': 'polar'}]])

# Adicionando o gráfico de radar para 2020
fig_m.add_trace(go.Scatterpolar(r=radar_data_2020['Média'], theta=radar_data_2020['Indicador'], 
                              fill='toself', name='2020'), row=1, col=1)

# Adicionando o gráfico de radar para 2021
fig_m.add_trace(go.Scatterpolar(r=radar_data_2021['Média'], theta=radar_data_2021['Indicador'], 
                              fill='toself', name='2021'), row=1, col=2)

# Adicionando o gráfico de radar para 2022
fig_m.add_trace(go.Scatterpolar(r=radar_data_2022['Média'], theta=radar_data_2022['Indicador'], 
                              fill='toself', name='2022'), row=1, col=3)

# Configurando o layout do gráfico sem títulos individuais de subplots
fig_m.update_layout(title_text='Perfil Médio dos Índices',
                  polar=dict(radialaxis=dict(visible=True)),
                  showlegend=True)

# Exibindo o gráfico
st.plotly_chart(fig_m)

st.divider()
# Gráfico 10: Comparação dos Índices ao Longo dos Anos

# Selecionando as colunas dos índices
indices = ['IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN', 'INDE']

# Calculando as médias dos índices para cada ano
medias_2020 = df_2020[indices].mean().reset_index()
medias_2020.columns = ['Indicador', 'Média 2020']

medias_2021 = df_2021[indices].mean().reset_index()
medias_2021.columns = ['Indicador', 'Média 2021']

medias_2022 = df_2022[indices].mean().reset_index()
medias_2022.columns = ['Indicador', 'Média 2022']

# Juntando as médias em um único DataFrame
medias_anos = pd.merge(medias_2020, medias_2021, on='Indicador')
medias_anos = pd.merge(medias_anos, medias_2022, on='Indicador')

# Transformando o DataFrame para o formato longo, necessário para o gráfico de linhas
medias_long = pd.melt(medias_anos, id_vars=['Indicador'], 
                      value_vars=['Média 2020', 'Média 2021', 'Média 2022'],
                      var_name='Ano', value_name='Média')

# Criando o gráfico de linhas para comparar os índices ao longo dos anos
fig_co = px.line(medias_long, x='Indicador', y='Média', color='Ano', 
              markers=True, title='Comparação dos Índices ao Longo dos Anos')

# Exibindo o gráfico
st.plotly_chart(fig_co)

st.divider()
# Gráfico 7: Alunos que Atingiram o Ponto de Virada

# Contando o número de alunos que atingiram o ponto de virada em cada ano
ponto_virada_2020 = df_2020[df_2020['PONTO_VIRADA'] == 'Sim']['NOME'].nunique()
ponto_virada_2021 = df_2021[df_2021['PONTO_VIRADA'] == 'Sim']['NOME'].nunique()
ponto_virada_2022 = df_2022[df_2022['PONTO_VIRADA'] == 'Sim']['NOME'].nunique()

# Contando o total de alunos em cada ano
total_alunos_2020 = df_2020['NOME'].nunique()
total_alunos_2021 = df_2021['NOME'].nunique()
total_alunos_2022 = df_2022['NOME'].nunique()

# Calculando a porcentagem de alunos que atingiram o ponto de virada
percentual_virada_2020 = (ponto_virada_2020 / total_alunos_2020) * 100
percentual_virada_2021 = (ponto_virada_2021 / total_alunos_2021) * 100
percentual_virada_2022 = (ponto_virada_2022 / total_alunos_2022) * 100

# Dados para o gráfico
anos = ['2020', '2021', '2022']
ponto_virada = [ponto_virada_2020, ponto_virada_2021, ponto_virada_2022]
percentual_virada = [percentual_virada_2020, percentual_virada_2021, percentual_virada_2022]

# Criando o gráfico com duplo eixo Y
fig_po = go.Figure()

# Adicionando a linha para o número de alunos que atingiram o ponto de virada
fig_po.add_trace(go.Scatter(
    x=anos,
    y=ponto_virada,
    mode='lines+markers',
    name='Número de Alunos',
    line=dict(width=4)
))

# Adicionando a linha para o percentual de alunos que atingiram o ponto de virada
fig_po.add_trace(go.Scatter(
    x=anos,
    y=percentual_virada,
    mode='lines+markers+text',
    name='Percentual',
    line=dict(width=4, dash='dash'),
    yaxis='y2',
    text=[f'{p:.2f}%' for p in percentual_virada],
    textposition='top center'
))

# Configurando o layout com duplo eixo Y
fig_po.update_layout(
    title='Alunos que Atingiram o Ponto de Virada',
    xaxis_title='Ano',
    yaxis=dict(
        title='Quantidade de Alunos'
    ),
    yaxis2=dict(
        title='Percentual',
        overlaying='y',
        side='right'
    ),
    legend=dict(x=0.1, y=0.9)
)


# Gráfico 11: Distribuição de Alunos por Nota de Português

# Calculando a média do INDE para cada ano
media_inde_2020 = df_2020['INDE'].mean()
media_inde_2021 = df_2021['INDE'].mean()
media_inde_2022 = df_2022['INDE'].mean()

# Verificando a evolução do INDE
evolucao_2020_2021 = (media_inde_2021 - media_inde_2020) / media_inde_2020 * 100
evolucao_2021_2022 = (media_inde_2022 - media_inde_2021) / media_inde_2021 * 100

# Criando um DataFrame para facilitar a plotagem
data = {
    'Ano': ['2020', '2021', '2022'],
    'Média INDE': [media_inde_2020, media_inde_2021, media_inde_2022]
}

df_media_inde = pd.DataFrame(data)

# Criando o gráfico de linha para mostrar a evolução do INDE
fig_ind = px.line(df_media_inde, x='Ano', y='Média INDE', 
              title='Evolução do INDE ao Longo dos Anos',
              markers=True)

# Criando duas colunas para exibir os gráficos lado a lado
col1, col2 = st.columns(2)

# Exibindo o primeiro gráfico na primeira coluna
with col1:
    st.plotly_chart(fig_po)

# Exibindo o segundo gráfico na segunda coluna
with col2:
    st.plotly_chart(fig_ind)
