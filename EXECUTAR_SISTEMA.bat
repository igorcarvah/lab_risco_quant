@echo off
chcp 65001 > nul
title LAB RISCO QUANT - MONITORAMENTO & DISTRIBUICAO

echo ========================================================
echo      🏦 LAB RISCO QUANT: AUTOMACAO FINANCEIRA 🚀
echo ========================================================
echo.
echo [1/3] 🔄 Conectando no Banco de Dados e Atualizando Cotacoes...
python src/scripts/etl_sql.py

echo.
echo [2/3] 📊 Calculando Riscos e Gerando Dashboard Excel...
python src/scripts/relatorio_excel.py

echo.
echo [3/3] 📧 Modulo de Distribuicao de Relatorios...
python src/scripts/enviar_email.py

echo.
echo ========================================================
echo ✅ CICLO COMPLETO FINALIZADO!
echo ========================================================
pause