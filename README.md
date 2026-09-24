# Consulta e exportação de projetos — Streamlit

Aplicativo independente, pronto para publicar no **Streamlit Community Cloud**. Inclui uma base **inteiramente fictícia** de **5.000 linhas e 7 colunas**, dois filtros de estado, um filtro de intervalo de datas e um filtro com cinco labels. Os botões exportam **somente as linhas filtradas** para Excel e PDF.

## Arquivos

```text
streamlit_exportacao_demo/
├── app.py                      # Página, filtros, tabela e botões
├── exportacao.py               # Criação do Excel e do PDF
├── dados/
│   └── projetos_ficticios.csv  # Base fictícia incluída
├── assets/
│   └── COLOQUE_A_LOGO_AQUI.txt
├── .streamlit/
│   └── config.toml             # Cores básicas
└── requirements.txt            # Dependências para o deploy
```

## Rodar no seu computador

Com Python 3.12 e um terminal aberto nesta pasta:

```bash
python -m venv .venv
```

No PowerShell do Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Em macOS ou Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Abra o endereço local indicado no terminal, normalmente `http://localhost:8501`.

## Inserir a logo da Embrapii

Coloque seu arquivo PNG nesta pasta com este nome exato:

```text
assets/logo_embrapii.png
```

O campo está no início do **app.py**:

```python
LOGO_EMBRAPII = PASTA / "assets" / "logo_embrapii.png"
```

Quando o arquivo existir, ele aparecerá no topo do aplicativo e em cada página do PDF. Se alterar o nome ou o local, atualize essa linha. Inclua o PNG no repositório ao publicar. Nenhuma imagem oficial foi adicionada ao projeto porque ela não foi fornecida.

## Publicar no Streamlit Community Cloud

1. Crie um repositório no GitHub e coloque **o conteúdo desta pasta na raiz** do repositório. Inclua `dados/projetos_ficticios.csv`, `exportacao.py`, `requirements.txt` e a logo, caso tenha adicionado uma.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e selecione **Create app**.
3. Escolha o repositório, a branch (por exemplo, `main`) e o arquivo principal **app.py**.
4. Em **Advanced settings**, selecione **Python 3.12**.
5. Inicie o deploy e abra a URL indicada quando terminar. O Community Cloud instala os pacotes do `requirements.txt` automaticamente.

**Os visitantes só precisam abrir a URL e clicar nos botões de download.** Não instalam Python nem bibliotecas.

## Trocar a base de exemplo

Substitua `dados/projetos_ficticios.csv` por um arquivo UTF-8 com separador `;` e os mesmos sete cabeçalhos:

```text
ID;Projeto;Estado de origem;Estado de destino;Data;Label;Valor (R$)
```

`Data` deve estar em `AAAA-MM-DD`; `Valor (R$)` é numérico, com ponto decimal e sem separador de milhares. Para mudar nomes, colunas ou origem dos dados, ajuste `carregar_dados()` e as referências dos filtros em `app.py`. Os dados do CSV incluído são fictícios e não representam projetos reais.

**Este aplicativo usa filtros próprios.** Ele não lê automaticamente os segmentadores do seu `.pbix` nem consulta o modelo publicado do Power BI. Para disponibilizar dados reais e atualizados, será preciso fornecer uma origem para o aplicativo ou atualizar o CSV no GitHub.

## Conferir o resultado

- Sem filtros, a tabela mostra **5.000 registros** e os dois botões exportam as mesmas 5.000 linhas.
- Selecione um estado de origem e outro de destino; a contagem e ambos os downloads diminuem.
- Ajuste as duas datas e selecione uma ou mais labels; os quatro filtros são aplicados juntos.
- Se nenhum registro corresponder, o Excel contém o cabeçalho e o PDF informa zero registros.
- No Excel, a primeira linha fica congelada e as colunas têm autofiltro; no PDF, o cabeçalho se repete em cada página.

Com todas as 5.000 linhas, o PDF da base demonstrativa tem aproximadamente **167 páginas**. A filtragem ajuda a produzir arquivos menores.

**Verificação feita:** os arquivos Excel e PDF foram gerados e reabertos com 5.000 registros, com seis registros após a combinação dos quatro filtros e com zero registros. O cabeçalho e a logo opcional foram conferidos no PDF. A execução visual pelo próprio Streamlit e o deploy no Community Cloud ainda precisam ser conferidos no seu ambiente, pois o pacote Streamlit não pôde ser instalado aqui.

As orientações de publicação seguem a [documentação oficial do Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). A lista de bibliotecas está em `requirements.txt`, conforme as [instruções para dependências](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).
