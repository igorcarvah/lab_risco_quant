import yfinance as yf
import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DE CAMINHOS ---
# Define onde o script está e onde o banco de dados deve ficar
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROJETO = os.path.dirname(DIRETORIO_SCRIPT)
PASTA_DADOS = os.path.join(RAIZ_PROJETO, "dados")
CAMINHO_DB = os.path.join(PASTA_DADOS, "mercado.db")

# Garante que a pasta 'dados' existe
if not os.path.exists(PASTA_DADOS):
    os.makedirs(PASTA_DADOS)

# Lista de Ativos para Monitoramento
CARTEIRA = [
    '^BVSP',      # Benchmark
    'VALE3.SA', 'PETR4.SA',  # Commodities
    'ITUB4.SA', 'BPAC11.SA', # Financeiro
    'MGLU3.SA', 'LREN3.SA',  # Varejo
    'WEGE3.SA', 'TAEE11.SA'  # Defensiva
]

def atualizar_banco_sql():
    print(f"🔌 Conectando ao Banco de Dados: {CAMINHO_DB}")
    conn = sqlite3.connect(CAMINHO_DB)
    
    print("⬇️  Baixando dados da B3 (Últimos 2 anos)...")
    # Pega data de hoje e volta 730 dias (2 anos)
    start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Baixa tudo de uma vez (Batch Download)
        dados = yf.download(CARTEIRA, start=start_date, end=end_date, progress=False)['Close']
        
        # Limpeza básica (remove dias vazios se houver falha na bolsa)
        dados.dropna(inplace=True)
        
        # SALVA NO SQL (A mágica acontece aqui)
        # 'replace' recria a tabela do zero para garantir dados frescos e limpos
        dados.to_sql('cotacoes', conn, if_exists='replace', index=True)
        
        print("✅ SUCESSO! Dados salvos na tabela SQL 'cotacoes'.")
        
        # Validando se salvou mesmo (Fazendo uma consulta de teste)
        check = pd.read_sql("SELECT count(*) as total FROM cotacoes", conn)
        print(f"📊 Total de registros salvos no banco: {check['total'][0]}")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar SQL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    atualizar_banco_sql()