from pathlib import Path

import streamlit as st

from exportacao import (
    COL_DATA, COLUNAS_NUMERICAS, filtrar_dados, gerar_excel, gerar_pdf,
    opcoes_disponiveis, preparar_dados,
)


PASTA = Path(__file__).resolve().parent
LOGO_EMBRAPII = PASTA / "assets" / "logo_embrapii.png"
ARQUIVO_DADOS = PASTA / "dados" / "projetos_embrapii.csv"

st.set_page_config(page_title="Projetos Embrapii | Consulta e exportação", layout="wide")


@st.cache_data(show_spinner="Carregando projetos...")
def carregar_dados(caminho: Path, modificado_em: int):
    return preparar_dados(caminho)


dados = carregar_dados(ARQUIVO_DADOS, ARQUIVO_DADOS.stat().st_mtime_ns)
colunas_filtraveis = list(dados.columns[2:])

if LOGO_EMBRAPII.is_file():
    st.image(str(LOGO_EMBRAPII), width=220)

st.title("Consulta de projetos Embrapii")
st.caption(f"Fonte: {ARQUIVO_DADOS.name} · {len(dados):,} registros · Use os filtros para consultar e exportar os resultados.".replace(",", "."))

st.subheader("Filtros")
st.caption("As opções de cada filtro acompanham as seleções feitas nos demais campos.")
datas = dados[COL_DATA].dt.date
data_minima, data_maxima = datas.min(), datas.max()
chave_periodo = "filtro_data_inicio"
if chave_periodo not in st.session_state:
    st.session_state[chave_periodo] = (data_minima, data_maxima)


def limpar_filtros():
    for coluna in colunas_filtraveis:
        if coluna != COL_DATA:
            st.session_state[f"filtro_{coluna}"] = []
    st.session_state[chave_periodo] = (data_minima, data_maxima)


st.button("Limpar todos os filtros", on_click=limpar_filtros)
periodo_salvo = st.session_state.get(chave_periodo, (data_minima, data_maxima))
periodo_para_opcoes = (
    tuple(periodo_salvo)
    if len(periodo_salvo) == 2 and tuple(periodo_salvo) != (data_minima, data_maxima)
    else None
)
selecoes_atuais = {
    coluna: st.session_state.get(f"filtro_{coluna}", [])
    for coluna in colunas_filtraveis
    if coluna != COL_DATA
}
filtros = {}

with st.container(border=True):
    colunas_ui = st.columns(3)
    for indice, coluna in enumerate(colunas_filtraveis):
        with colunas_ui[indice % 3]:
            if coluna == COL_DATA:
                periodo_escolhido = st.date_input(
                    coluna,
                    min_value=data_minima,
                    max_value=data_maxima,
                    format="DD/MM/YYYY",
                    key=chave_periodo,
                )
            else:
                opcoes = opcoes_disponiveis(dados, coluna, selecoes_atuais, periodo_para_opcoes)
                # Valores já escolhidos continuam visíveis para que possam ser removidos.
                opcoes = list(set(opcoes).union(selecoes_atuais[coluna]))
                opcoes = sorted(opcoes, key=lambda valor: valor if coluna in COLUNAS_NUMERICAS else str(valor).casefold())
                filtros[coluna] = st.multiselect(coluna, opcoes, placeholder="Todos", key=f"filtro_{coluna}")

if len(periodo_escolhido) != 2:
    st.info("Selecione também a data final para aplicar o período.")
    st.stop()

periodo_ativo = tuple(periodo_escolhido) if tuple(periodo_escolhido) != (data_minima, data_maxima) else None
filtrado = filtrar_dados(dados, filtros, periodo_ativo)

st.metric("Projetos encontrados", f"{len(filtrado):,}".replace(",", "."))
st.dataframe(
    filtrado,
    hide_index=True,
    width="stretch",
    height=520,
    column_config={COL_DATA: st.column_config.DateColumn(COL_DATA, format="DD/MM/YYYY")},
)

if filtrado.empty:
    st.info("Nenhum projeto corresponde aos filtros. Os arquivos conterão o cabeçalho e o resumo da consulta.")

origem_app = st.context.url
download_excel, download_pdf = st.columns(2)
with download_excel:
    st.download_button(
        "Extrair para Excel",
        data=lambda: gerar_excel(filtrado),
        file_name="projetos_embrapii_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        on_click="ignore",
        width="stretch",
    )
with download_pdf:
    st.download_button(
        "Extrair para PDF",
        data=lambda: gerar_pdf(filtrado, LOGO_EMBRAPII, filtros, periodo_ativo, origem_app),
        file_name="projetos_embrapii_filtrados.pdf",
        mime="application/pdf",
        on_click="ignore",
        width="stretch",
    )
