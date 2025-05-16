
# Mega-Sena Inteligente

Este é um app em Streamlit que gera cartões da Mega-Sena com base em filtros estatísticos e permite comparar com o último resultado oficial.

## Funcionalidades

- Geração de cartões únicos com 6 dezenas
- Histórico dos jogos gerados durante a sessão
- Exportação dos jogos em TXT e PDF
- Atualização automática do último resultado da Mega-Sena via scraping

## Como usar

1. Instale as dependências:

```
pip install -r requirements.txt
```

2. Atualize o último resultado manualmente ou rode:

```
python atualizar_resultado.py
```

3. Rode o app:

```
streamlit run app.py
```

## Agendamento

Para atualizar automaticamente o resultado, agende o script `atualizar_resultado.py` para rodar periodicamente usando cron (Linux/Mac) ou Agendador de Tarefas (Windows).

