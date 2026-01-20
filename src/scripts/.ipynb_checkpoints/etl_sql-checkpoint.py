import yfinance as yf
import pandas as pd
import sqlite3
import os

# Configuração de Caminhos
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROJETO = os.path.dirname(os.path.dirname(DIRETORIO_ATUAL))
CAMINHO_DB = os.path.join(RAIZ_PROJETO, "dados", "mercado.db")

TICKERS = [
    '^BVSP', 'VALE3.SA', 'PETR4.SA', 'ITUB4.SA', 'BPAC11.SA',
    'MGLU3.SA', 'LREN3.SA', 'WEGE3.SA', 'TAEE11.SA'
]

def atualizar_banco():
    # Cria a pasta dados se não existir
    if not os.path.exists(os.path.dirname(CAMINHO_DB)):
        os.makedirs(os.path.dirname(CAMINHO_DB))

    print(f"🔄 Baixando dados para: {len(TICKERS)} ativos...")
    try:
        # CORREÇÃO: auto_adjust=False garante que as colunas venham no formato padrão
        df = yf.download(TICKERS, period="2y", progress=False, auto_adjust=False)
        
        # Tratamento seguro da coluna de preços
        if 'Adj Close' in df.columns:
            dados = df['Adj Close']
        elif 'Close' in df.columns:
            dados = df['Close']
        else:
            print("❌ Erro: Coluna de preço não encontrada no retorno do Yahoo.")
            return

        # Salva no SQL
        conn = sqlite3.connect(CAMINHO_DB)
        dados.to_sql("cotacoes", conn, if_exists="replace", index=True)
        conn.close()
        print("✅ Banco de Dados atualizado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro Crítico no ETL: {e}")

if __name__ == "__main__":
    atualizar_banco()