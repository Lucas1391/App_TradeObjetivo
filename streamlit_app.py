import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas_ta as ta
from PIL import Image

image = Image.open("TRADE.png")
st.image(image,width=100)

st.title("APP GRÁFICO TRADEOBJETIVO")
indicadores = ['IFR2','MEDIA3-MAX&MIN','TUTLE 20/10','SETUP 9.1']
Indicador = st.sidebar.selectbox('Escolha o indicador desejado :',indicadores)
ativo = st.sidebar.text_input("Digite o ativo desejado : ")
if ativo:
    df = yf.download(ativo, period='60d')
    #Analisando setup escolhido
    if Indicador == indicadores[0]:
        df['IFR2'] = ta.rsi(df['Close'],length=2)
        df['Buy'] = np.where(df["IFR2"] > 25 , df['Close'] ,np.nan)
        df['Highest'] = df['High'].rolling(2).max()
        df['Highest'] = df['Highest'].shift(1)
        df['Sell'] = np.where(df['Close'] > df['Highest'] ,df["Close"] ,np.nan)
        df['parametro'] = 25.00
        #gráfico bbas3 (candlestick
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
                'width': 3,
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

        #informar todos os dados e gráficos em uma lista
        data = [trace1, trace2, trace3, trace4]

        #configurar o layout do gráfico
        layout = go.Layout({
            'title': {
            'text': f'Gráfico IFR2 {ativo}',
            'font': {
                'size': 20
                }
            }
        })

        #instanciar objeto Figure e plotar o gráfico
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
        #configurar o layout do gráfico
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
