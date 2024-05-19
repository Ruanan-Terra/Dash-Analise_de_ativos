import yfinance
import pandas as pd
import pandas_datareader.data as pdr
from datetime import datetime, timedelta
import plotly.express as px

yfinance.pdr_override()

def pega_acao(ativo, data_inicio = None, data_fim = None):
    if data_inicio == None:
        data_inicio = datetime.now() - timedelta(365)

    if data_fim == None:
        data_fim = datetime.now()

    resultantList = ["^BVSP"]

    for ativo_list in ativo:
        if ativo_list not in resultantList:
            resultantList.append(ativo_list)

    df_acoes = pd.DataFrame()

    for acao in resultantList:
        df = pdr.get_data_yahoo(acao,data_inicio, data_fim)
        df['Ativo'] = acao
        df.reset_index(inplace=True)
        df_acoes = pd.concat([df_acoes, df], ignore_index=True)
        df_acoes.reset_index(inplace=True, drop=True)

    
    df_acoes.to_parquet("geral_ativo.parquet")
    
    return df_acoes

def retorno_mm(df, colunas):
    df_retorno = pd.DataFrame()

    df_values  = df[df['Ativo'].isin(list(colunas))]
    resultantList = df_values['Ativo'].unique()

    for acao in resultantList:

        df_ret = df.copy()
        df_ret.reset_index(inplace=True)
        df_ret['Retorno'] = (df_ret['Adj Close'] / df_ret['Adj Close'][0]) -1
        df_retorno = pd.concat([df_retorno, df_ret], ignore_index=True)

    return df_retorno
    
if __name__ == "__main__":
    ativo = ["BTC-USD", "BBDC4.SA", "ITUB4.SA"]
    pega_acao(ativo = ativo)

    geral = pd.read_parquet("geral_ativo.parquet")
