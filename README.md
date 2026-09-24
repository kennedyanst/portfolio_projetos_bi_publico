# Consulta e exportação de projetos — Streamlit

Aplicativo independente, pronto para publicar no **Streamlit Community Cloud**. Inclui uma base **inteiramente fictícia** de **5.000 linhas e 7 colunas**, dois filtros de estado, um filtro de intervalo de datas e um filtro com cinco labels. Os botões exportam **somente as linhas filtradas** para Excel e PDF.

## Arquivos

```text
portfolio_projetos_bi_publico/
├── app.py                      # Página, filtros, tabela e botões
├── exportacao.py               # Criação do Excel e do PDF
├── dados/
│   └── projetos_ficticios.csv  # Base fictícia incluída
├── assets/
│   ├── logo_embrapii.png       # Logo usada no app e no PDF
│   └── COLOQUE_A_LOGO_AQUI.txt
├── .streamlit/
│   └── config.toml             # Cores básicas
└── requirements.txt            # Dependências para o deploy
```

## Rodar no seu computador

Com Python 3.13 ou 3.14 e um terminal aberto nesta pasta (o deploy atual usa 3.14):

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

O PNG incluído no repositório aparece no topo do aplicativo e em cada página do PDF. Se alterar o nome ou o local, atualize essa linha e inclua o novo arquivo no repositório.

## Publicar no Streamlit Community Cloud

1. Crie um repositório no GitHub e coloque **o conteúdo desta pasta na raiz** do repositório. Inclua `dados/projetos_ficticios.csv`, `exportacao.py`, `requirements.txt` e a logo, caso tenha adicionado uma.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e selecione **Create app**.
3. Escolha o repositório, a branch (por exemplo, `main`) e o arquivo principal **app.py**.
4. Em **Advanced settings**, selecione **Python 3.14** para usar a mesma versão de Python para a qual as dependências foram preparadas.
5. Inicie o deploy e abra a URL indicada quando terminar. O Community Cloud instala os pacotes do `requirements.txt` automaticamente.

Se o aplicativo já está publicado com Python 3.14, basta enviar a alteração do `requirements.txt` ao GitHub: o Community Cloud detecta a mudança nas dependências e faz um novo deploy. Não é necessário recriar o aplicativo. A versão de Python de um aplicativo já criado só pode ser alterada ao excluí-lo e publicá-lo novamente.

**Os visitantes só precisam abrir a URL e clicar nos botões de download.** Excel e PDF são gerados apenas no clique; os visitantes não instalam Python nem bibliotecas.

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

**Verificação local:** com Python 3.13 e pandas 2.3.3, o aplicativo abriu sem erro e sem gerar os arquivos antes do clique; o Excel foi reaberto com 5.000 registros e o PDF gerado foi validado. A resolução das dependências para Linux com Python 3.14 também foi conferida sem instalar pacotes. O deploy no Community Cloud deve ser conferido após o commit.

As orientações de publicação seguem a [documentação oficial do Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). A lista de bibliotecas está em `requirements.txt`, conforme as [instruções para dependências](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).
