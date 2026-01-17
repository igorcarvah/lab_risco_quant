import yfinance as yf
import pandas as pd
import sqlite3
import os

# Configuração
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROJETO = os.path.dirname(os.path.dirname(DIRETORIO_ATUAL))
CAMINHO_DB = os.path.join(RAIZ_PROJETO, "dados", "mercado.db")

tickers = ['^BVSP', 'VALE3.SA', 'PETR4.SA', 'ITUB4.SA', 'BPAC11.SA', 
           'MGLU3.SA', 'LREN3.SA', 'WEGE3.SA', 'TAEE11.SA']

print("📥 Baixando dados...")
dados = yf.download(tickers, start="2020-01-01", progress=False)['Close']
dados.columns = tickers # Corrige MultiIndex se necessário

# Salvar no SQL
if not os.path.exists(os.path.dirname(CAMINHO_DB)):
    os.makedirs(os.path.dirname(CAMINHO_DB))

conn = sqlite3.connect(CAMINHO_DB)
dados.to_sql("cotacoes", conn, if_exists="replace")
conn.close()
print("