import pandas as pd
import scipy.stats
import numpy as np

# ==============================================================================
# MÓDULO DE CÁLCULO DE RISCO (QUANT LIBRARY)
# Desenvolvido para o Projeto Lab de Mercado Financeiro
# Baseado na metodologia EDHEC Risk Institute
# ==============================================================================

# 1. BIBLIOTECA QUANT (DEFINIÇÕES MATEMÁTICAS)

def total_return(r):
    """Calcula o Retorno Total Acumulado (Ex: 0.50 para 50%)."""
    return (1 + r).prod() - 1

def annualize_rets(r, periods_per_year):
    """Calcula o Retorno Anualizado (CAGR)."""
    compounded_growth = (1 + r).prod()
    n_periods = r.shape[0]
    return compounded_growth**(periods_per_year/n_periods) - 1

def annualize_vol(r, periods_per_year):
    """
    Calcula a Volatilidade Anualizada.
    (Esta era a função que FALTAVA no seu código original!)
    """
    return r.std() * (periods_per_year**0.5)

def sharpe_ratio(r, riskfree_rate, periods_per_year):
    """
    Calcula o Sharpe Ratio.
    Agora funciona pois annualize_rets e annualize_vol já existem acima.
    """
    ret_asset = annualize_rets(r, periods_per_year)
    vol_asset = annualize_vol(r, periods_per_year)
    return (ret_asset - riskfree_rate) / vol_asset

def drawdown(return_series: pd.Series):
    """Calcula Drawdown, Wealth Index e Picos."""
    wealth_index = 1000 * (1 + return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    return pd.DataFrame({"Wealth": wealth_index, "Previous Peak": previous_peaks, "Drawdown": drawdowns})

def skewness(r):
    """
    Calcula a Assimetria (Skewness).
    Viés estatístico dos retornos.
    Negativo = Maior chance de perdas extremas do que ganhos extremos.
    """
    demeaned_r = r - r.mean()
    # Usamos o desvio padrão populacional (ddof=0) para seguir o padrão Quant
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp / sigma_r**3

def kurtosis(r):
    """
    Calcula a Curtose (Kurtosis).
    Mede a 'gordura' das caudas.
    3.0 = Distribuição Normal.
    > 3.0 = Caudas Gordas (Risco de eventos extremos/Cisnes Negros).
    """
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp / sigma_r**4


def var_historic(r, level=5):
    """
    Retorna o VaR Histórico (Value at Risk) em um certo nível percentual.
    Ex: level=5 significa que estamos olhando para os 5% piores casos da história.
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, level=level)
    elif isinstance(r, pd.Series):
        # Multiplica por -1 para retornar um número positivo (perda positiva)
        return -np.percentile(r, level)
    else:
        raise TypeError("Expected r to be Series or DataFrame")

def var_gaussian(r, level=5, modified=False):
    """
    Retorna o VaR Paramétrico (Gaussiano).
    
    Parâmetros:
    - modified (bool): 
        - Se True: Retorna o VaR Cornish-Fisher (ajustado para caudas gordas/Assimetria e Curtose).
        - Se False: Retorna o VaR Normal padrão (assume curva de sino).
    """
    # Computa o Z-score baseado na distribuição normal (ex: 1.65 para 5%)
    z = scipy.stats.norm.ppf(level/100)
    
    if modified:
        # Modificação de Cornish-Fisher: Ajusta o Z baseado na "loucura" real dos dados
        s = skewness(r)
        k = kurtosis(r)
        z = (z +
             (z**2 - 1)*s/6 +
             (z**3 - 3*z)*(k-3)/24 -
             (2*z**3 - 5*z)*(s**2)/36
            )
    
    # Fórmula: Média + (Z * Desvio Padrão)
    # Colocamos o sinal negativo para expressar a perda como valor positivo
    return -(r.mean() + z*r.std(ddof=0))

def cvar_historic(r, level=5):
    """
    Calcula o CVaR (Conditional VaR) Histórico.
    Também conhecido como: Expected Shortfall (ES) ou "Beyond VaR".
    
    O que ele responde: "Nos piores 5% dos dias, qual é a MÉDIA do prejuízo?"
    É muito mais agressivo e realista que o VaR comum.
    """
    if isinstance(r, pd.Series):
        # 1. Descobre quanto é o VaR Histórico
        is_beyond = r <= -var_historic(r, level=level)
        # 2. Calcula a média de tudo que for PIOR que o VaR
        return -r[is_beyond].mean()
    elif isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_historic, level=level)
    else:
        raise TypeError("Expected r to be Series or DataFrame")
