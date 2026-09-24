from pathlib import Path

import pandas as pd
import streamlit as st

from exportacao import filtrar_dados, gerar_excel, gerar_pdf


PASTA = Path(__file__).resolve().parent
# Coloque seu PNG neste local para aparecer no aplicativo e no PDF.
LOGO_EMBRAPII = PASTA / "assets" / "logo_embrapii.png"
ARQUIVO_DADOS = PASTA / "dados" / "projetos_ficticios.csv"

st.set_page_config(page_title="Projetos | Consulta e exportação", layout="wide")


@st.cache_data
def carregar_dados():
    return pd.read_csv(ARQUIVO_DADOS, sep=";", encoding="utf-8-sig", parse_dates=["Data"])


dados = carregar_dados()

if LOGO_EMBRAPII.is_file():
    st.image(str(LOGO_EMBRAPII), width=220)

st.title("Consulta de projetos")
st.caption("Demonstração com 5.000 registros fictícios. Os downloads respeitam os filtros selecionados.")

estados = sorted(set(dados["Estado de origem"]) | set(dados["Estado de destino"]))
labels = sorted(dados["Label"].unique())

col1, col2, col3, col4 = st.columns(4)
with col1:
    origem = st.selectbox("Estado de origem", ["Todos"] + estados)
with col2:
    destino = st.selectbox("Estado de destino", ["Todos"] + estados)
with col3:
    periodo = st.date_input(
        "Período da data",
        value=(dados["Data"].min().date(), dados["Data"].max().date()),
        min_value=dados["Data"].min().date(),
        max_value=dados["Data"].max().date(),
        format="DD/MM/YYYY",
    )
with col4:
    labels_escolhidos = st.multiselect("Labels (5 opções)", labels)

if len(periodo) != 2:
    st.info("Selecione também a data final para aplicar o período.")
    st.stop()

filtrado = filtrar_dados(dados, origem, destino, periodo, labels_escolhidos)

st.metric("Projetos encontrados", f"{len(filtrado):,}".replace(",", "."))
st.dataframe(
    filtrado,
    hide_index=True,
    use_container_width=True,
    height=520,
    column_config={
        "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
        "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f"),
    },
)

if filtrado.empty:
    st.info("Nenhum projeto corresponde aos filtros. Os arquivos conterão apenas o cabeçalho.")

download_excel, download_pdf = st.columns(2)
with download_excel:
    st.download_button(
        "Extrair para Excel",
        data=gerar_excel(filtrado),
        file_name="projetos_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
with download_pdf:
    st.download_button(
        "Extrair para PDF",
        data=gerar_pdf(filtrado, LOGO_EMBRAPII),
        file_name="projetos_filtrados.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
