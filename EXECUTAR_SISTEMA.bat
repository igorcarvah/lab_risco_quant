@echo off
chcp 65001 > nul
echo ========================================================
echo      LAB RISCO QUANT - SISTEMA DE ANALISE DE MERCADO
echo ========================================================
echo.

:: PASSO 1: Atualização (Com verificação de erro)
echo 1. Atualizando Base de Dados (ETL)...
:: Tenta rodar na pasta scripts. Se não achar, tenta na raiz src.
if exist "src/scripts/etl_sql.py" (
    python src/scripts/etl_sql.py
) else (
    echo [AVISO] Script ETL nao encontrado em src/scripts. Tentando rodar apenas o relatorio...
)
echo.

:: PASSO 2: Geração do Relatório
echo 2. Calculando Riscos e Gerando Relatorio...
python src/scripts/relatorio_excel.py
echo.

:: PASSO 3: Abrir o Excel Automaticamente (O Pulo do Gato)
echo 3. Abrindo o relatorio gerado...
cd reports
:: Este comando pega o último arquivo .xlsx criado (o mais novo)
for /f "delims=" %%x in ('dir /b /od *.xlsx') do set "UltimoArquivo=%%x"
start "" "%UltimoArquivo%"
cd ..

echo ========================================================
echo ✅ SUCESSO! O Excel deve abrir na sua tela agora.
echo ========================================================
pause