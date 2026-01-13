import pandas as pd

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
    

