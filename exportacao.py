from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import pandas as pd


COL_ESTADO_UNIDADE = "Estado da Unidade Embrapii"
COL_ESTADO_EMPRESA = "Estado da Empresa"
COL_INSTITUICAO = "Instituição"


def filtrar_dados(dados, origem, destino, periodo, labels):
    filtrado = dados.loc[dados["Data"].dt.date.between(periodo[0], periodo[1])]
    if origem != "Todos":
        filtrado = filtrado.loc[filtrado[COL_ESTADO_UNIDADE] == origem]
    if destino != "Todos":
        filtrado = filtrado.loc[filtrado[COL_ESTADO_EMPRESA] == destino]
    if labels:
        filtrado = filtrado.loc[filtrado[COL_INSTITUICAO].isin(labels)]
    return filtrado


def gerar_excel(dados: pd.DataFrame) -> bytes:
    arquivo = BytesIO()
    with pd.ExcelWriter(arquivo, engine="openpyxl", datetime_format="DD/MM/YYYY") as writer:
        dados.to_excel(writer, sheet_name="Projetos", index=False)
        aba = writer.sheets["Projetos"]
        aba.freeze_panes = "A2"
        aba.auto_filter.ref = aba.dimensions
        for letra, largura in {"A": 12, "B": 46, "C": 22, "D": 22, "E": 16, "F": 22, "G": 19}.items():
            aba.column_dimensions[letra].width = largura
    return arquivo.getvalue()


def gerar_pdf(dados: pd.DataFrame, logo=None) -> bytes:
    arquivo = BytesIO()
    pdf = canvas.Canvas(arquivo, pagesize=landscape(A4), pageCompression=1)
    pdf.setTitle("Projetos filtrados")
    largura_pagina, altura_pagina = landscape(A4)
    titulos = ["ID", "Projeto", "UF Unidade", "UF Empresa", "Data", "Instituição", "Valor (R$)"]
    larguras = [38, 218, 68, 68, 68, 120, 100]
    inicio_x = 31

    def cabecalho(numero_pagina):
        if numero_pagina > 1:
            pdf.showPage()
        titulo_x = 31
        if logo is not None and logo.is_file():
            pdf.drawImage(str(logo), 31, altura_pagina - 63, width=115, height=36, preserveAspectRatio=True, mask="auto")
            titulo_x = 160
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(titulo_x, altura_pagina - 42, "Projetos filtrados")
        pdf.setFont("Helvetica", 9)
        pdf.drawString(titulo_x, altura_pagina - 59, f"{len(dados):,} registros".replace(",", "."))
        y = altura_pagina - 91
        pdf.setFillColor(colors.HexColor("#125C49"))
        pdf.rect(inicio_x, y - 5, sum(larguras), 19, fill=1, stroke=0)
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 8)
        x = inicio_x
        for titulo, largura in zip(titulos, larguras):
            pdf.drawString(x + 4, y + 1, titulo)
            x += largura
        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica", 8)
        return y - 20

    pagina = 1
    y = cabecalho(pagina)
    for linha in dados.itertuples(index=False, name=None):
        if y < 42:
            pdf.setFont("Helvetica", 8)
            pdf.drawRightString(largura_pagina - 31, 24, f"Página {pagina}")
            pagina += 1
            y = cabecalho(pagina)
        id_projeto, projeto, origem, destino, data, label, valor = linha
        campos = [
            str(id_projeto), str(projeto)[:48], str(origem), str(destino),
            pd.Timestamp(data).strftime("%d/%m/%Y"), str(label),
            f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        ]
        x = inicio_x
        for campo, largura in zip(campos, larguras):
            if x == inicio_x + sum(larguras[:-1]):
                pdf.drawRightString(x + largura - 5, y, campo)
            else:
                pdf.drawString(x + 4, y, campo)
            x += largura
        y -= 15
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(largura_pagina - 31, 24, f"Página {pagina}")
    pdf.save()
    return arquivo.getvalue()
