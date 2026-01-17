# 🏦 Lab Risco Quant: Monitor de Risco de Mercado & Cisnes Negros

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)
![University](https://img.shields.io/badge/Universidade-Anhembi%20Morumbi-red)
![Methodology](https://img.shields.io/badge/Methodology-EDHEC%20Business%20School-darkblue)
![Domain](https://img.shields.io/badge/Finance-Risk%20Management-orange)


> **"A volatilidade é o preço da admissão. A ruína é o risco a ser evitado."**

Este projeto é um laboratório prático de **Engenharia Financeira** e **Automação de Processos (RPA)**. O objetivo foi construir um pipeline "End-to-End" que monitora ativos da B3, calcula métricas avançadas de risco e gera relatórios de auditoria automaticamente.

---

## 🎯 O Problema de Negócio

Em gestão de portfólio, olhar apenas para a **Volatilidade** (Desvio Padrão) é insuficiente. O verdadeiro perigo para o capital reside nos **Eventos de Cauda (Cisnes Negros)** — movimentos extremos e raros que quebram modelos tradicionais.

Este software resolve isso criando um **Sistema de Alerta Antecipado** que:
1.  **Centraliza Dados:** Baixa e armazena histórico de preços em banco SQL local.
2.  **Mede o Invisível:** Calcula *Kurtosis* (Curtose) e *Skewness* para detectar caudas gordas.
3.  **Entrega Valor:** Gera um Dashboard Excel "Pixel Perfect" pronto para a diretoria, sem necessidade de intervenção manual.

---

## 📊 O Produto Final (Dashboard)

O sistema gera um arquivo Excel com design profissional, contendo:

### 1. Zona de Dados & Métricas
Cálculo automatizado de **VaR 95%**, **Sharpe Ratio** e **Max Drawdown** para ativos selecionados (IBOV, VALE3, PETR4, etc.).

### 2. O "Detector de Cisne Negro"
Um algoritmo analisa a distribuição estatística dos retornos. Se a **Kurtosis for > 3**, o sistema aciona um **ALERTA CRÍTICO** visual (Caixa Vermelha), indicando que aquele ativo possui alta probabilidade de eventos extremos.

### 3. Visualização de Eficiência
Gráfico de dispersão (Scatter Plot) gerado nativamente pelo Python dentro do Excel, cruzando Risco (Volatilidade) x Retorno.

---

## 📸 Screenshots

*(Exemplo do Relatório Gerado Automaticamente)*

![Dashboard Preview](reports/excel_final1.png)
![Dashboard Preview](reports/excel_final2.png)
![Dashboard Preview](reports/excel_final3.png)

---

## 🛠️ Arquitetura Técnica

O projeto segue princípios de **Governança de Dados** e **Clean Code**, separando a lógica em camadas:

```text
LAB_RISCO_QUANT/
├── dados/                   # Data Lake (SQLite + Arquivos Brutos)
│   └── mercado.db           # Banco de Dados Histórico (Persistência)
├── reports/                 # Saída dos Relatórios (.xlsx)
├── src/                     # Código Fonte
│   └── scripts/             
│       ├── etl_sql.py       # Camada de Ingestão (YFinance -> SQL)
│       └── relatorio_excel.py # Motor de Cálculo e Renderização Excel
├── EXECUTAR_SISTEMA.bat     # Executável "One-Click" para usuário final
├── README.md                # Documentação
└── requirements.txt         # Dependências do Python


# Clone o repositório
git clone https://github.com/igorcarvah/lab_risco_quant.git

# Instale as dependências
pip install pandas numpy matplotlib seaborn scipy yfinance

