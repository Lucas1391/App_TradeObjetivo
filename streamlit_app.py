import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas_ta as ta

ativos = ['AAPL',
 'MSFT',
 'AMZN',
 'FB',
 'GOOGL',
 'GOOG',
 'BRK-B',
 'JPM',
 'JNJ',
 'TSLA',
 'UNH',
 'V',
 'NVDA',
 'HD',
 'PG',
 'BAC',
 'MA',
 'DIS',
 'PYPL',
 'XOM',
 'CMCSA',
 'VZ',
 'ADBE',
 'INTC',
 'T',
 'PFE',
 'CSCO',
 'NFLX',
 'CVX',
 'KO',
 'ABT',
 'ABBV',
 'MRK',
 'PEP',
 'WFC',
 'CRM',
 'WMT',
 'ACN',
 'AVGO',
 'TMO',
 'NKE',
 'MCD',
 'COST',
 'MDT',
 'TXN',
 'C',
 'DHR',
 'HON',
 'LIN',
 'UPS',
 'LLY',
 'PM',
 'UNP',
 'QCOM',
 'ORCL',
 'BMY',
 'AMGN',
 'LOW',
 'NEE',
 'CAT',
 'MS',
 'RTX',
 'SBUX',
 'IBM',
 'GS',
 'BA',
 'BLK',
 'DE',
 'MMM',
 'GE',
 'INTU',
 'AMAT',
 'AMT',
 'CVS',
 'SCHW',
 'TGT',
 'AXP',
 'CHTR',
 'ANTM',
 'LMT',
 'ISRG',
 'MO',
 'CI',
 'FIS',
 'BKNG',
 'AMD',
 'SPGI',
 'MU',
 'NOW',
 'MDLZ',
 'GILD',
 'TJX',
 'USB',
 'LRCX',
 'PLD',
 'PNC',
 'TFC',
 'ADP',
 'SYK',
 'TMUS',
 'ZTS',
 'COP',
 'DUK',
 'CCI',
 'CME',
 'CSX',
 'CB',
 'FDX',
 'COF',
 'NSC',
 'ATVI',
 'GM',
 'CL',
 'BDX',
 'SHW',
 'ITW',
 'MMC',
 'SO',
 'EL',
 'FISV',
 'APD',
 'FCX',
 'EQIX',
 'ICE',
 'D',
 'PGR',
 'ADSK',
 'NEM',
 'BSX',
 'ETN',
 'GPN',
 'HUM',
 'NOC',
 'AON',
 'EMR',
 'VRTX',
 'EW',
 'HCA',
 'ILMN',
 'REGN',
 'ECL',
 'WM',
 'ADI',
 'MCO',
 'NXPI',
 'DOW',
 'DG',
 'EOG',
 'MET',
 'SLB',
 'F',
 'JCI',
 'DD',
 'KLAC',
 'ROST',
 'ROP',
 'KMB',
 'LHX',
 'IDXX',
 'AIG',
 'GD',
 'TEL',
 'IQV',
 'EXC',
 'TT',
 'TROW',
 'SYY',
 'PRU',
 'BIIB',
 'PPG',
 'AEP',
 'ALL',
 'PSA',
 'BK',
 'TWTR',
 'BAX',
 'DLR',
 'SRE',
 'HPQ',
 'CNC',
 'PH',
 'TRV',
 'ALGN',
 'SPG',
 'STZ',
 'MPC',
 'EBAY',
 'APH',
 'WBA',
 'A',
 'EA',
 'CMI',
 'ORLY',
 'PSX',
 'INFO',
 'MCHP',
 'ALXN',
 'GIS',
 'ADM',
 'MSCI',
 'APTV',
 'CTSH',
 'CMG',
 'XEL',
 'MAR',
 'LUV',
 'KMI',
 'DFS',
 'AFL',
 'CARR',
 'SNPS',
 'YUM',
 'IFF',
 'SWK',
 'ZBH',
 'CTVA',
 'WLTW',
 'CDNS',
 'AZO',
 'GLW',
 'MSI',
 'HLT',
 'MNST',
 'VLO',
 'FRC',
 'PXD',
 'TDG',
 'PCAR',
 'OTIS',
 'WMB',
 'PAYX',
 'MCK',
 'NUE',
 'DHI',
 'SBAC',
 'PEG',
 'DXCM',
 'CTAS',
 'AME',
 'FAST',
 'ROK',
 'WELL',
 'FITB',
 'STT',
 'WEC',
 'AMP',
 'SIVB',
 'DAL',
 'LYB',
 'MTD',
 'CBRE',
 'BLL',
 'XLNX',
 'EFX',
 'ES',
 'WY',
 'KR',
 'KHC',
 'RMD',
 'AJG',
 'VRSK',
 'VFC',
 'ANSS',
 'BBY',
 'FTNT',
 'AVB',
 'AWK',
 'DTE',
 'SWKS',
 'KSU',
 'ED',
 'LEN',
 'LH',
 'KEYS',
 'ODFL',
 'DLTR',
 'ZBRA',
 'VMC',
 'CPRT',
 'SYF',
 'EQR',
 'HSY',
 'IP',
 'NTRS',
 'URI',
 'MXIM',
 'OKE',
 'O',
 'WST',
 'FTV',
 'CDW',
 'TSN',
 'HIG',
 'HES',
 'CERN',
 'MLM',
 'WDC',
 'EXPE',
 'RSG',
 'KEY',
 'CLX',
 'FLT',
 'VIAC',
 'RF',
 'PPL',
 'MKC',
 'OXY',
 'ARE',
 'CCL',
 'EIX',
 'VRSN',
 'TSCO',
 'CHD',
 'DOV',
 'CFG',
 'MTB',
 'HPE',
 'XYL',
 'ETR',
 'HAL',
 'GRMN',
 'STX',
 'CZR',
 'AEE',
 'ETSY',
 'GWW',
 'FE',
 'EXPD',
 'VTR',
 'IT',
 'KMX',
 'TER',
 'VTRS',
 'QRVO',
 'TTWO',
 'TDY',
 'CE',
 'WAT',
 'AMCR',
 'BKR',
 'TRMB',
 'GPC',
 'COO',
 'EXR',
 'NDAQ',
 'BR',
 'ESS',
 'LVS',
 'ULTA',
 'AKAM',
 'RCL',
 'GNRC',
 'CAG',
 'ALB',
 'TFX',
 'AVY',
 'IR',
 'CMS',
 'DRI',
 'J',
 'CINF',
 'UAL',
 'MAA',
 'PEAK',
 'OMC',
 'ANET',
 'EMN',
 'DGX',
 'POOL',
 'NTAP',
 'ABC',
 'MKTX',
 'IEX',
 'PFG',
 'CTLT',
 'K',
 'NVR',
 'AES',
 'DPZ',
 'STE',
 'DRE',
 'CAH',
 'LB',
 'RJF',
 'MAS',
 'WRK',
 'HBAN',
 'HOLX',
 'DVN',
 'CRL',
 'PKI',
 'MGM',
 'TYL',
 'PAYC',
 'BXP',
 'TXT',
 'PHM',
 'WHR',
 'INCY',
 'FMC',
 'NLOK',
 'XRAY',
 'ENPH',
 'FBHS',
 'PKG',
 'JBHT',
 'SJM',
 'FANG',
 'CTXS',
 'LUMN',
 'AAL',
 'WAB',
 'LKQ',
 'BF-B',
 'LNT',
 'EVRG',
 'LDOS',
 'UDR',
 'CNP',
 'SNA',
 'PTC',
 'AAP',
 'PWR',
 'L',
 'MPWR',
 'CHRW',
 'TPR',
 'HWM',
 'WYNN',
 'HRL',
 'MHK',
 'MOS',
 'IPG',
 'BIO',
 'LNC',
 'ALLE',
 'IRM',
 'UHS',
 'ATO',
 'BWA',
 'FOXA',
 'HAS',
 'HST',
 'LYV',
 'ABMD',
 'CBOE',
 'PENN',
 'JKHY',
 'CF',
 'HSIC',
 'LW',
 'PNR',
 'DISH',
 'FFIV',
 'WRB',
 'NWL',
 'CMA',
 'TAP',
 'RE',
 'NWSA',
 'NCLH',
 'IVZ',
 'WU',
 'RHI',
 'GL',
 'NLSN',
 'REG',
 'CPB',
 'ZION',
 'NI',
 'MRO',
 'PNW',
 'AOS',
 'BEN',
 'AIZ',
 'DXC',
 'DISCK',
 'KIM',
 'DVA',
 'ALK',
 'SEE',
 'HII',
 'JNPR',
 'APA',
 'NRG',
 'PVH',
 'PBCT',
 'ROL',
 'FRT',
 'GPS',
 'LEG',
 'COG',
 'VNO',
 'IPGP',
 'NOV',
 'HBI',
 'RL',
 'UNM',
 'PRGO',
 'FOX',
 'HFC',
 'DISCA',
 'UAA',
 'UA',
 'NWS']
indicadores = ['IFR2','MEDIA3-MAX&MIN','TUTLE 20/10','SETUP 9.1']
Indicador = st.sidebar.selectbox('Escolha o indicador desejado :',indicadores)
ativo = st.sidebar.selectbox("Escolha o ticker desejado :",ativos)
df = yf.download(ativo,period='60d')
#image = Image.open(r"C:\Users\Lenovo\Pictures\TRADE.png")
#st.image(image,width=500)
st.title("APP GRÁFICO TRADEOBJETIVO")
#Analisando setup escolhido
if Indicador == indicadores[0]:
    df['IFR2'] = ta.rsi(df['Close'],length=2)
    df['Buy'] = np.where(df["IFR2"] > 25 , df['Close'] ,np.nan)
    df['Highest'] = df['High'].rolling(2).max()
    df['Highest'] = df['Highest'].shift(1)
    df['Sell'] = np.where(df['Close'] > df['Highest'] ,df["Close"] ,np.nan)
    df['parametro']  = 25.00
    # gráfico bbas3 (candlestick
    trace1 = {
        'x': df.index,
        'open': df['Open'],
        'close': df['Close'],
        'high': df['High'],
        'low': df['Low'],
        'type': 'candlestick',
        'name': f'{ativo}',
        'showlegend': False
    }
    # média de 30 dias (linha)
    trace2 = {
        'x': df.index,
        'y':  df['Highest'],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'Highest2'
    }

    trace3 = {
        'x': df.index,
        'y': df['Buy'],
        'type': 'scatter',
        'mode': 'markers + text',
        'line': {
            'width': 2,
            'color': 'pink'
        },
        'name': 'Buy'
    }

    trace4 = {
        'x': df.index,
        'y': df['Sell'],
        'type': 'scatter',
        'mode': 'markers + text',
        'line': {
            'width': 2,
            'color': 'orange'
        },
        'name': 'Sell'
    }

    # informar todos os dados e gráficos em uma lista
    data = [trace1, trace2, trace3, trace4]

    # configurar o layout do gráfico
    layout = go.Layout({
        'title': {
            'text': f'Gráfico IFR2 {ativo}',
            'font': {
                'size': 20
            }
        }
    })

    # instanciar objeto Figure e plotar o gráfico
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, width=300, height=300)

    trace5 = {
        'x': df.index,
        'y': df['IFR2'],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'IFR2'
    }

    trace6 = {
        'x': df.index,
        'y':df['parametro'],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'red'
        },
        'name': 'Nível sobrecomprado'
    }
    data_1 = [trace5,trace6]
    # configurar o layout do gráfico
    layout_1 = go.Layout({
        'title': {
            'text': f'Indicador IFR2 {ativo}',
            'font': {
                'size': 20
            }
        }
    })

    fig_1 = go.Figure(data=data_1, layout=layout_1)
    st.plotly_chart(fig_1,width=100, height=50)

elif Indicador == indicadores[1]:
    df['Avg_Low3'] = df['Low'].rolling(3).mean()
    df['Avg_Low3'] = df['Avg_Low3'].shift(1)
    df['Avg_High3'] = df['High'].rolling(3).mean()
    df['Avg_High3'] = df['Avg_High3'].shift(1)
    df['Buy'] = np.where(df["Close"] < df["Avg_Low3"] , df['Close'] ,np.nan)
    df['Sell'] = np.where(df["Close"] > df["Avg_High3"], df["Close"] ,np.nan)
    # gráfico bbas3 (candlestick
    trace1 = {
        'x': df.index,
        'open': df['Open'],
        'close': df['Close'],
        'high': df['High'],
        'low': df['Low'],
        'type': 'candlestick',
        'name': f'{ativo}',
        'showlegend': False
        }
    #média de 30 dias (linha)
    trace2 = {
        'x': df.index,
        'y': df['Avg_Low3'] ,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'Média (3 Min)'
    }

    trace3 = {
        'x': df.index,
        'y': df['Avg_High3'],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
        'width': 1,
        'color': 'yellow'
        },
        'name': 'Média (3 Max)'
    }

    trace4 = {
        'x': df.index,
        'y': df['Buy'],
        'type': 'scatter',
        'mode':  'markers + text',
        'line': {
            'width': 2,
            'color': 'pink'
        },
        'name': 'Buy'
    }

    trace5 = {
        'x': df.index,
        'y': df['Sell'],
        'type': 'scatter',
        'mode':  'markers + text',
        'line': {
            'width': 2,
            'color': 'orange'
        },
        'name': 'Sell'
    }

    #informar todos os dados e gráficos em uma lista
    data = [trace1,trace2,trace3,trace4,trace5]

    # configurar o layout do gráfico
    layout = go.Layout({
        'title': {
            'text': f'Gráfico 3 Máx/mín {ativo}',
            'font': {
            'size': 20
            }
        }
    })

    #instanciar objeto Figure e plotar o gráfico
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart (fig,width = 300,height=300)

elif Indicador == indicadores[2]:
    df['Highest 20'] = df['High'].rolling(20).max()
    df['Highest 20'] = df['Highest 20'].shift(1)
    df['Lowest 10'] = df['Low'].rolling(10).min()
    df['Lowest 10'] = df['Lowest 10'].shift(1)
    df['Buy'] = np.where(df["Close"] > df["Highest 20"], df['Close'], np.nan)
    df['Sell'] = np.where(df["Close"] < df["Lowest 10"], df["Close"], np.nan)

    # gráfico bbas3 (candlestick
    trace1 = {
        'x': df.index,
        'open': df['Open'],
        'close': df['Close'],
        'high': df['High'],
        'low': df['Low'],
        'type': 'candlestick',
        'name': f'{ativo}',
        'showlegend': False
    }
    # média de 30 dias (linha)
    trace2 = {
        'x': df.index,
        'y': df['Lowest 10'],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'Lowest 10'
    }

    trace3 = {
        'x': df.index,
        'y': df['Highest 20'],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'yellow'
        },
        'name': 'Highest 20'
    }

    trace4 = {
        'x': df.index,
        'y': df['Buy'],
        'type': 'scatter',
        'mode': 'markers + text',
        'line': {
            'width': 2,
            'color': 'pink'
        },
        'name': 'Buy'
    }

    trace5 = {
        'x': df.index,
        'y': df['Sell'],
        'type': 'scatter',
        'mode': 'markers + text',
        'line': {
            'width': 2,
            'color': 'orange'
        },
        'name': 'Sell'
    }

    # informar todos os dados e gráficos em uma lista
    data = [trace1, trace2, trace3, trace4, trace5]

    # configurar o layout do gráfico
    layout = go.Layout({
        'title': {
            'text': f'Gráfico Tutle 20/10 {ativo}',
            'font': {
                'size': 20
            }
        }
    })

    # instanciar objeto Figure e plotar o gráfico
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, width=300, height=300)
else:
    #Média de 9.1
    df['avg_exp 9'] = df['Close'].ewm(span=9, min_periods=9).mean()
    df['avg_exp 9'] = df['avg_exp 9'].shift(1)
    df['Buy'] = np.where(df["Close"] > df["avg_exp 9"], df['Close'], np.nan)
    df['Sell'] = np.where(df["Close"] < df["avg_exp 9"], df["Close"], np.nan)

    # gráfico bbas3 (candlestick
    trace1 = {
        'x': df.index,
        'open': df['Open'],
        'close': df['Close'],
        'high': df['High'],
        'low': df['Low'],
        'type': 'candlestick',
        'name': f'{ativo}',
        'showlegend': False
    }
    # média de 30 dias (linha)
    trace2 = {
        'x': df.index,
        'y': df['avg_exp 9'],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'media exp 9'
    }


    trace3 = {
        'x': df.index,
        'y': df['Buy'],
        'type': 'scatter',
        'mode': 'markers + text',
        'line': {
            'width': 2,
            'color': 'pink'
        },
        'name': 'Buy'
    }

    trace4 = {
        'x': df.index,
        'y': df['Sell'],
        'type': 'scatter',
        'mode': 'markers + text',
        'line': {
            'width': 2,
            'color': 'orange'
        },
        'name': 'Sell'
    }

    # informar todos os dados e gráficos em uma lista
    data = [trace1, trace2, trace3, trace4]

    # configurar o layout do gráfico
    layout = go.Layout({
        'title': {
            'text':f'Gráfico 9.1 {ativo}',
            'font': {
                'size': 20
            }
        }
    })

    # instanciar objeto Figure e plotar o gráfico
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, width=300, height=300)





