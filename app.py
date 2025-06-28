import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os

st.set_page_config(page_title="Monitoramento Sphenophorus", layout="wide")
st.title("📊 Monitoramento de Sphenophorus")

# Carregar dados
df = pd.read_excel('./data/Base de levantamento Sphenophorus.xlsx', sheet_name='Ficha de campo_Sphenophorus', header=1)


colunas_uso = [
    'Cod_Cliente', 'Nome_Cliente', 'Fazenda', 'Data_Avaliacao',
    'Tratamento', 'Densidade_Populacional', 'Tocos_Analisados',
    'Tocos_Atacados', 'Infestacao',
    'Foto_1', 'Info_Foto_1', 'Foto_2', 'Info_Foto_2', 'Foto_3', 'Info_Foto_3'
]
df = df[colunas_uso].dropna(subset=['Tratamento', 'Data_Avaliacao'])

with st.sidebar:
    st.header("🔍 Filtros")
    cliente = st.multiselect("Cliente", df['Nome_Cliente'].dropna().unique())
    fazenda = st.multiselect("Fazenda", df['Fazenda'].dropna().unique())
    tratamento = st.multiselect("Tratamento", df['Tratamento'].dropna().unique())
    datas = st.multiselect("Data de Avaliação", df['Data_Avaliacao'].dropna().unique())

# Aplicar filtros
df_filtrado = df.copy()
if cliente:
    df_filtrado = df_filtrado[df_filtrado['Nome_Cliente'].isin(cliente)]
if fazenda:
    df_filtrado = df_filtrado[df_filtrado['Fazenda'].isin(fazenda)]
if tratamento:
    df_filtrado = df_filtrado[df_filtrado['Tratamento'].isin(tratamento)]
if datas:
    df_filtrado = df_filtrado[df_filtrado['Data_Avaliacao'].isin(datas)]

# KPIs
st.subheader("📌 Indicadores Gerais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Média de Infestação", f"{df_filtrado['Infestacao'].mean():.2f}")
col2.metric("Tocos Analisados", f"{df_filtrado['Tocos_Analisados'].sum():,.0f}")
col3.metric("Tocos Atacados", f"{df_filtrado['Tocos_Atacados'].sum():,.0f}")
col4.metric("Densidade Populacional Média", f"{df_filtrado['Densidade_Populacional'].mean():.2f}")

# Botões de exportação
st.sidebar.markdown("---")
st.sidebar.subheader("📄 Exportar Dados")

# Exportar CSV
df_csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📄 Baixar CSV",
    data=df_csv,
    file_name='dados_filtrados.csv',
    mime='text/csv'
)

# Exportar Excel
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_filtrado.to_excel(writer, index=False, sheet_name='Filtrado')
    writer.close()
    st.sidebar.download_button(
        label="📈 Baixar Excel",
        data=output.getvalue(),
        file_name='dados_filtrados.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Gráfico 1: Densidade Populacional
st.subheader("📌 Densidade Populacional por Tratamento")
densidade = df_filtrado.groupby(['Tratamento', 'Data_Avaliacao'])['Densidade_Populacional'].sum().reset_index()
st.dataframe(densidade)
fig1 = px.bar(densidade, x='Tratamento', y='Densidade_Populacional', color='Data_Avaliacao', barmode='group')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Tocos Analisados vs Atacados
st.subheader("📌 Tocos Analisados vs Atacados")
tocos = df_filtrado.groupby('Tratamento')[['Tocos_Analisados', 'Tocos_Atacados']].mean().reset_index()
st.dataframe(tocos)
fig2 = px.bar(tocos, x='Tratamento', y=['Tocos_Analisados', 'Tocos_Atacados'], barmode='group')
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Infestação ao longo do tempo
st.subheader("📌 Infestação ao Longo do Tempo")
infestacao = df_filtrado.groupby(['Data_Avaliacao', 'Tratamento'])['Infestacao'].sum().reset_index()
st.dataframe(infestacao)
fig3 = px.line(infestacao, x='Data_Avaliacao', y='Infestacao', color='Tratamento', markers=True)
st.plotly_chart(fig3, use_container_width=True)

# Painel de Fotos corrigido com filtros completos
st.subheader("📸 Fotos do Levantamento")
if df_filtrado.empty:
    st.info("Nenhum registro encontrado com os filtros selecionados.")
else:
    df_fotos = df.copy()
    df_fotos = df_fotos[
        (df_fotos['Nome_Cliente'].isin(df_filtrado['Nome_Cliente'].unique())) &
        (df_fotos['Fazenda'].isin(df_filtrado['Fazenda'].unique())) &
        (df_fotos['Data_Avaliacao'].isin(df_filtrado['Data_Avaliacao'].unique())) &
        (df_fotos['Tratamento'].isin(df_filtrado['Tratamento'].unique()))
    ]
    agrupado = df_fotos.groupby(['Nome_Cliente', 'Fazenda', 'Data_Avaliacao'])
    for (cliente_sel, fazenda_sel, data_sel), grupo in agrupado:
        st.markdown(f"### 📍 {cliente_sel} - {fazenda_sel} ({data_sel.strftime('%d/%m/%Y')})")
        for idx, row in grupo.iterrows():
            with st.expander(f"Tratamento: {row['Tratamento']}"):
                cols = st.columns(3)
                for i, foto_col in enumerate(['Foto_1', 'Foto_2', 'Foto_3']):
                    if pd.notna(row[foto_col]):
                        nome_arquivo = str(row[foto_col]).strip()
                        foto_path = os.path.join("fotos_sphenophorus", nome_arquivo)
                        info_col = f"Info_{foto_col}"
                        if os.path.exists(foto_path) or foto_path.startswith("http"):
                            with cols[i]:
                                st.image(foto_path, caption=row.get(info_col, ""), use_container_width=True)
                        else:
                            with cols[i]:
                                st.warning(f"Imagem inválida ou não encontrada: {foto_path}")