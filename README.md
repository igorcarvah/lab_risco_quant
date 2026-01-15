# 🔬 Lab Risco Quant: Análise Estatística da B3

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![University](https://img.shields.io/badge/Universidade-Anhembi%20Morumbi-red?style=flat)
![Methodology](https://img.shields.io/badge/Methodology-EDHEC%20Business%20School-darkblue?style=flat)

> *"No mercado financeiro, retorno é vaidade, risco é sanidade."*

Este projeto é um laboratório de **Estatística e Finanças Quantitativas** que aplica a metodologia do curso *Investment Management with Python* da **EDHEC Business School** para analisar o comportamento real de ativos brasileiros (IBOVESPA, Vale, Petrobras, etc.).

O objetivo é ir além da rentabilidade nominal e explorar a anatomia do risco, servindo como parte do portfólio acadêmico do curso de **Estatística da Universidade Anhembi Morumbi**.

---

## 📖 O Problema (Storytelling)

Muitos investidores olham apenas para o gráfico de subida (Retorno). Porém, dois ativos podem entregar o mesmo retorno de 10% ao ano, mas com "viagens" completamente diferentes. Um pode ser uma estrada tranquila (baixa volatilidade), o outro uma montanha-russa emocional (alta volatilidade e *drawdowns* profundos).

**A pergunta que este projeto responde é:**
> *Qual o custo (risco) que estou pagando por cada unidade de retorno que recebo? E quais ativos escondem riscos extremos (Caudas Gordas) que a média simples não mostra?*

---

## 🤖 Diferencial: Automação & Reporting

Além da modelagem estatística, o projeto conta com um módulo de **Business Intelligence Automatizado**.
Sabendo que em mesas de operações a tomada de decisão precisa ser rápida e visual, desenvolvi um pipeline de entrega executiva:

* **Automação com Python (`openpyxl`):** Scripts dedicados calculam métricas complexas e geram Dashboards em Excel formatados automaticamente.
* **Detecção de Anomalias:** O relatório aplica formatação condicional, destacando em **vermelho** ativos com Assimetria Negativa e em **negrito** ativos com "Caudas Gordas" (Kurtosis > 3), alertando o gestor sobre riscos ocultos.

---

## 📐 Fundamentação Matemática (The Quant Engine)

O projeto não utiliza apenas bibliotecas prontas; os cálculos foram implementados matematicamente em um módulo proprietário (`src/metricas_risco.py`) para garantir precisão e entendimento dos fundamentos.

### 1. Retorno Ajustado ao Risco (Sharpe Ratio)
Utilizamos o índice de Sharpe para medir a eficiência da alocação.
$$Sharpe = \frac{R_p - R_f}{\sigma_p}$$
Onde $R_f$ (Risk Free) foi assumido como proxy do CDI/SELIC.

### 2. Momentos Estatísticos (Além da Curva Normal)
O mercado não segue perfeitamente uma Distribuição Normal (Gaussiana). Para capturar o "Risco de Cauda" (Cisnes Negros), calculamos os momentos superiores:

* **Assimetria (Skewness - 3º Momento):** Mede se o risco é maior para o lado negativo (quedas abruptas).
  $$Skew = E\left[\left(\frac{X - \mu}{\sigma}\right)^3\right]$$

* **Curtose (Kurtosis - 4º Momento):** Identifica "Caudas Gordas". Se $Kurtosis > 3$, o ativo possui probabilidade elevada de eventos extremos (crises).
  $$Kurt = E\left[\left(\frac{X - \mu}{\sigma}\right)^4\right]$$

### 3. Drawdown (A Dor do Investidor)
Mede a queda percentual do topo histórico até o fundo. Essencial para gestão de risco psicológico e de capital.

---

## 🛠️ Arquitetura e Engenharia de Dados

O projeto segue princípios de **Engenharia de Software** para Ciência de Dados:

* **Modularização:** O código principal (`notebooks/*.ipynb`) atua apenas como orquestrador. A lógica pesada reside na pasta `src/`.
* **Automação:** Scripts de rotina ficam isolados na pasta `scripts/` para fácil execução.
* **ETL & Persistência:**
    * Extração via API `yfinance`.
    * Tratamento de MultiIndex e limpeza de dados.
    * **Data Governance:** Os dados são salvos localmente, garantindo reprodutibilidade.

### Estrutura de Pastas
```text
lab-risco-quant/
│
├── 📁 dados/                  # Data Lake local (CSVs/ZIPs)
├── 📁 notebooks/              # O Painel de Controle (Visualização/Jupyter)
│   └── 01_analise_caudas.ipynb
│
├── 📁 reports/                # Relatórios Excel gerados automaticamente
│   └── Relatorio_Risco_Quant_YYYYMMDD.xlsx
│
├── 📁 scripts/                # Scripts de Automação e Tarefas Agendadas
│   └── gerar_relatorio.py
│
├── 📁 src/                    # O "Cérebro" do projeto (Bibliotecas internas)
│   ├── __init__.py
│   ├── dados_mercado.py       # ETL e Carga de dados
│   └── metricas_risco.py      # Fórmulas Matemáticas (Kurtosis, Skewness, etc.)
│
├── LICENSE                    # Licença MIT
└── README.md                  # Documentação

# Clone o repositório
git clone https://github.com/igorcarvah/lab_risco_quant.git

# Instale as dependências
pip install pandas numpy matplotlib seaborn scipy yfinance

