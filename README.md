# Consulta e exportação de projetos Embrapii

Aplicativo Streamlit para consultar os dados de `dados/projetos_embrapii.csv` e exportar os resultados filtrados para Excel ou PDF.

## Dados e filtros

O CSV usa UTF-8, separador `;` e contém 16 colunas. As duas primeiras, `Título Público do Projeto` e `Descrição`, aparecem na tabela e nos arquivos exportados, mas não são filtros. Cada uma das outras 14 colunas tem um filtro: `Data de Inicio` usa intervalo de datas; as demais permitem selecionar um ou mais valores. Sem seleção, o filtro não restringe os resultados. As opções de cada campo acompanham os demais filtros ativos; valores já selecionados permanecem visíveis para que possam ser removidos. O botão **Limpar todos os filtros** remove as seleções e restaura o intervalo completo de datas.

Os filtros disponíveis incluem status, empresa contratante, porte, UF, projetos contratados, segmento CEIS, unidade Embrapii, TRL inicial e final, níveis de área de aplicação e tecnologia habilitadora.

O Excel preserva todas as colunas e as linhas filtradas. O PDF apresenta um bloco por projeto, com título, descrição e os outros 14 campos. No início do PDF aparecem os filtros aplicados, a quantidade de projetos, a fonte dos dados, a URL do aplicativo usada na extração e a data e hora em UTC. O rodapé repete a fonte, a data e hora e o número da página. Textos longos quebram em linhas e podem continuar na página seguinte.

## Executar localmente

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Em macOS ou Linux, use `.venv/bin/python` no lugar de `.venv\Scripts\python.exe`.

## Publicar

Publique `app.py` no Streamlit Community Cloud com `requirements.txt`, `exportacao.py`, `dados/projetos_embrapii.csv` e, se desejar, `assets/logo_embrapii.png`. O aplicativo lê o CSV incluído no repositório; ele não consulta a API FastAPI. Antes de publicar, confirme que a versão do CSV no repositório pode ser disponibilizada aos usuários do aplicativo.
