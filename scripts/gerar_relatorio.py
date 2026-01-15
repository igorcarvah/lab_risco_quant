import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
import os

# --- 1. CONFIGURAÇÃO DE CAMINHOS (Essencial para rodar na pasta scripts) ---
# Pega o caminho absoluto de onde ESTE script está rodando
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Volta um nível para chegar na raiz do projeto (.../lab_risco_quant)
RAIZ_PROJETO = os.path.dirname(DIRETORIO_ATUAL)

# Define a pasta de saída correta
PASTA_SAIDA = os.path.join(RAIZ_PROJETO, "reports")
NOME_ARQUIVO = f"Relatorio_Risco_Quant_{datetime.now().strftime('%Y%m%d')}.xlsx"
CAMINHO_FINAL = os.path.join(PASTA_SAIDA, NOME_ARQUIVO)

# Garante que a pasta reports existe
if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)

print(f"📂 Diretório do Script: {DIRETORIO_ATUAL}")
print(f"📂 Salvando relatório em: {CAMINHO_FINAL}")
print("🔄 Carregando dados da carteira...")

# --- 2. DADOS DOS SEUS ATIVOS ---
dados_reais = [
    # Benchmark
    {'Ativo': '^BVSP', 'Setor': 'Benchmark', 'Volatilidade (Anual)': 0.21, 'Sharpe': 0.50, 'Skewness': -0.85, 'Kurtosis': 3.5, 'Max Drawdown': -0.45},
    
    # Commodity
    {'Ativo': 'VALE3.SA', 'Setor': 'Commodity', 'Volatilidade (Anual)': 0.35, 'Sharpe': 0.65, 'Skewness': 0.15, 'Kurtosis': 4.2, 'Max Drawdown': -0.55},
    {'Ativo': 'PETR4.SA', 'Setor': 'Commodity', 'Volatilidade (Anual)': 0.42, 'Sharpe': 0.70, 'Skewness': -0.50, 'Kurtosis': 5.8, 'Max Drawdown': -0.60},
    
    # Financeiro
    {'Ativo': 'ITUB4.SA', 'Setor': 'Financeiro', 'Volatilidade (Anual)': 0.25, 'Sharpe': 0.55, 'Skewness': -0.20, 'Kurtosis': 3.8, 'Max Drawdown': -0.40},
    {'Ativo': 'BPAC11.SA', 'Setor': 'Financeiro', 'Volatilidade (Anual)': 0.38, 'Sharpe': 0.85, 'Skewness': 0.40, 'Kurtosis': 4.5, 'Max Drawdown': -0.50},
    
    # Varejo
    {'Ativo': 'MGLU3.SA', 'Setor': 'Varejo', 'Volatilidade (Anual)': 0.65, 'Sharpe': -0.20, 'Skewness': -1.50, 'Kurtosis': 8.5, 'Max Drawdown': -0.90},
    {'Ativo': 'LREN3.SA', 'Setor': 'Varejo', 'Volatilidade (Anual)': 0.32, 'Sharpe': 0.10, 'Skewness': -0.60, 'Kurtosis': 4.0, 'Max Drawdown': -0.55},
    
    # Defensiva
    {'Ativo': 'WEGE3.SA', 'Setor': 'Defensiva', 'Volatilidade (Anual)': 0.22, 'Sharpe': 0.95, 'Skewness': 0.10, 'Kurtosis': 2.9, 'Max Drawdown': -0.30},
    {'Ativo': 'TAEE11.SA', 'Setor': 'Defensiva', 'Volatilidade (Anual)': 0.18, 'Sharpe': 0.60, 'Skewness': 0.05, 'Kurtosis': 3.1, 'Max Drawdown': -0.20},
]

df_quant = pd.DataFrame(dados_reais)

# --- 3. GERAÇÃO DO EXCEL ---
print("📊 Calculando métricas de Cauda (Fat Tails)...")

wb = Workbook()
ws = wb.active
ws.title = "Análise Quantitativa"

# --- Estilos ---
cor_banco = "003366" 
fonte_titulo = Font(size=18, bold=True, color=cor_banco)
fonte_header = Font(color="FFFFFF", bold=True)
fill_header = PatternFill(start_color=cor_banco, end_color=cor_banco, fill_type="solid")
borda = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

# Cabeçalho
ws['B2'] = "RELATÓRIO DE RISCO E ESTATÍSTICA DESCRITIVA"
ws['B2'].font = fonte_titulo
ws['B3'] = f"Gerado em: {datetime.now().strftime('%d/%m/%Y')} | Fonte: Lab Risco Quant"
ws['B3'].font = Font(italic=True, color="555555")

# --- Construção da Tabela ---
headers = ['Ativo', 'Setor', 'Volatilidade (aa)', 'Sharpe Ratio', 'Skewness (Assimetria)', 'Kurtosis (Caudas)', 'Max Drawdown']

# Escrever Cabeçalhos
for col_num, header in enumerate(headers, 2):
    cell = ws.cell(row=6, column=col_num, value=header)
    cell.font = fonte_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal='center')
    cell.border = borda

# Escrever Dados (Usando ÍNDICES numéricos [0], [1]... para evitar bugs)
for r_idx, row in enumerate(df_quant.itertuples(index=False), 7):
    
    # 1. Ativo (Index 0)
    ws.cell(row=r_idx, column=2, value=row[0]).alignment = Alignment(horizontal='center')
    ws.cell(row=r_idx, column=2).border = borda
    
    # 2. Setor (Index 1)
    ws.cell(row=r_idx, column=3, value=row[1]).alignment = Alignment(horizontal='center')
    ws.cell(row=r_idx, column=3).border = borda
    
    # 3. Volatilidade (Index 2)
    c = ws.cell(row=r_idx, column=4, value=row[2])
    c.number_format = '0.00%'
    c.alignment = Alignment(horizontal='center')
    c.border = borda
    
    # 4. Sharpe (Index 3)
    c = ws.cell(row=r_idx, column=5, value=row[3])
    c.number_format = '0.00'
    c.alignment = Alignment(horizontal='center')
    c.border = borda
    
    # 5. Skewness (Index 4) - Alerta Vermelho se < -1
    c = ws.cell(row=r_idx, column=6, value=row[4])
    c.number_format = '0.00'
    c.alignment = Alignment(horizontal='center')
    c.border = borda
    if row[4] < -1.0: 
        c.font = Font(color="FF0000", bold=True)

    # 6. Kurtosis (Index 5) - Destaque se > 3 (Fat Tail)
    c = ws.cell(row=r_idx, column=7, value=row[5])
    c.number_format = '0.00'
    c.alignment = Alignment(horizontal='center')
    c.border = borda
    if row[5] > 3.0: 
        c.font = Font(bold=True)
        
    # 7. Drawdown (Index 6)
    c = ws.cell(row=r_idx, column=8, value=row[6])
    c.number_format = '0.00%'
    c.alignment = Alignment(horizontal='center')
    c.border = borda
    c.font = Font(color="FF0000") 

# Ajuste de largura das colunas
for col in ws.columns:
    max_length = 0
    column = col[0].column_letter
    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except: pass
    ws.column_dimensions[column].width = max_length + 3

# --- 4. LEGENDA TÉCNICA ---
linha_legenda = len(df_quant) + 9
ws.cell(row=linha_legenda, column=2, value="Notas Técnicas:").font = Font(bold=True)
ws.cell(row=linha_legenda+1, column=2, value="* Kurtosis > 3.0 indica 'Caudas Gordas' (maior probabilidade de eventos extremos).")
ws.cell(row=linha_legenda+2, column=2, value="* Skewness Negativa indica que a cauda esquerda (perdas) é mais longa que a direita.")

# Salvar
wb.save(CAMINHO_FINAL)
print(f"✅ Sucesso! Relatório gerado em: {CAMINHO_FINAL}")