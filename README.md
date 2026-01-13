# 🔬 Lab Risco Quant: Análise Estatística da B3

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)
![University](https://img.shields.io/badge/Universidade-Anhembi%20Morumbi-red)
![Methodology](https://img.shields.io/badge/Methodology-EDHEC%20Business%20School-darkblue)

> *"No mercado financeiro, retorno é vaidade, risco é sanidade."*

Este projeto é um laboratório de **Estatística e Finanças Quantitativas** que aplica a metodologia do curso *Investment Management with Python* da **EDHEC Business School** para analisar o comportamento real de ativos brasileiros (IBOVESPA, Vale, Petrobras, Varejo, etc.).

O objetivo é ir além da rentabilidade nominal e explorar a anatomia do risco, servindo como parte do portfólio acadêmico do curso de **Estatística da Universidade Anhembi Morumbi**.

---

## 📖 O Problema (Storytelling)

Muitos investidores olham apenas para o gráfico de subida (Retorno). Porém, dois ativos podem entregar o mesmo retorno de 10% ao ano, mas com "viagens" completamente diferentes. Um pode ser uma estrada tranquila (baixa volatilidade), o outro uma montanha-russa emocional (alta volatilidade e *drawdowns* profundos).

**A pergunta que este projeto responde é:**
> *Qual o custo (risco) que estou pagando por cada unidade de retorno que recebo? E quais ativos escondem riscos extremos (Caudas Gordas) que a média simples não mostra?*

---

## 📐 Fundamentação Matemática (The Quant Engine)

O projeto não utiliza apenas bibliotecas prontas; os cálculos foram implementados matematicamente em um módulo proprietário (`src/dados_mercado.py`) para garantir precisão e entendimento dos fundamentos.

### 1. Retorno Ajustado ao Risco (Sharpe Ratio)
Utilizamos o índice de Sharpe para medir a eficiência da alocação.
$$Sharpe = \frac{R_p - R_f}{\sigma_p}$$
Onde $R_f$ (Risk Free) foi assumido como 10% a.a. (Proxy SELIC/CDI).

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

* **Modularização:** O código principal (`analise_portfolio.ipynb`) atua apenas como orquestrador e visualizador. Toda a lógica pesada reside no módulo `src/dados_mercado.py`.
* **ETL & Persistência:**
    * Extração via API `yfinance`.
    * Tratamento de MultiIndex e limpeza de dados.
    * **Data Governance:** Os dados são salvos localmente em formato compactado (`.zip`), garantindo reprodutibilidade e performance, evitando dependência constante da API.
* **Hot-Reloading:** Uso de *magic commands* do Jupyter para desenvolvimento ágil do módulo.

### Estrutura de Pastas
```text
lab-risco-quant/
├── analise_portfolio.ipynb  # O Painel de Controle (Visualização)
├── dados/                   # Armazenamento local (Data Lake simples)
│   └── cotacoes_acoes.zip
└── src/                     # O "Cérebro" do projeto
    ├── __init__.py
    └── dados_mercado.py     # Fórmulas e Funções

---

## 📊 Visualizações Geradas

O notebook gera um Dashboard completo contendo:
1.  **Wealth Index:** Evolução de R$ 1.000,00 investidos no tempo.
2.  **Drawdown Chart:** Visualização das "cicatrizes" (quedas) de cada ativo.
3.  **Teste de Normalidade:** Histograma dos retornos reais sobreposto à Curva Normal teórica (evidenciando as caudas gordas).
4.  **Mapa de Calor (Heatmap):** Matriz de correlação para análise de diversificação.
5.  **Scatter Plot (Risco x Retorno):** Mapa de eficiência para identificar os ativos "Campeões" (Alto Retorno, Baixo Risco).

---

## 🚀 Como Executar

### Pré-requisitos
* Python 3.8+
* Jupyter Notebook

### Instalação
```bash
# Clone o repositório
git clone [https://github.com/igorcarvah/lab_risco_quant.git]

# Instale as dependências
pip install pandas numpy matplotlib seaborn scipy yfinance