#Instalando Pacotes
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas_ta as ta
from PIL import Image

#===========================================PROGRAMA AQUI=================================================
#Carregando Logomarca
image = Image.open("TRADE.png")
#Abrindo logomarca no Streamlit
#st.image(image,width=200)
#Iniciando APP
st.title("APLICATIVO GRÁFICO TRADEOBJETIVO")
#Indicadores disponíveis
indicadores = ['','IFR2','MEDIA3-MAX&MIN','TUTLE 20/10','SETUP 9.1',"SUPERTREND","DOCHIAN 10","BANDAS DE BOLLINGER"]
#Indicador para o usuário selecionar
Indicador = st.sidebar.selectbox('Escolha o indicador desejado :',indicadores)
#Digitar o ativo desejado
ativo = st.sidebar.text_input("Digite o ativo desejado : ")
#============================================================================FUNÇAO OPERAÇÕES========================================================================
def Operacoes(n,df):
    resultado_compras = []
    #listas de vendas
    resultado_vendas = []
    tam = len(df)
    #parametro boleano para não comprar duas veses seguidas
    flag_compra = False
    #marcação do ultima dia compra
    dia_ultima_compra = 0
    for i in range(n,tam):
        if (podeComprar(i,df)) and (not flag_compra):
            linha = [df.index[i],df['Close'][i]]
            resultado_compras.append(linha)
            flag_compra = True
            dia_ultima_compra=i
          #lista de vendas 
        elif (podeVender(i,df)) and (flag_compra):
            linha1 = [df.index[i],df['Close'][i]]
            resultado_vendas.append(linha1)
            flag_compra = False  
    resultado_compras = pd.DataFrame(resultado_compras,columns = ["Data","Price_Buy"])
    resultado_vendas = pd.DataFrame(resultado_vendas,columns = ["Data","Price_Sell"])
    compras = resultado_compras['Price_Buy'].tolist()
    vendas = resultado_vendas['Price_Sell'].tolist()
    lista_compras = []
    lista_vendas = []
    for i in range(0,len(df)):
        if (df['Close'][i] in compras):
            lista_compras.append(df['Close'][i])
        else:
            lista_compras.append(np.NaN)
    for j in range(0,len(df)):
        if (df['Close'][j] in vendas):
            lista_vendas.append(df['Close'][j])
        else:
            lista_vendas.append(np.NaN)

    df['Buy'] = lista_compras
    df['Sell'] = lista_vendas
    return df

#=======================================================================FUNÇOES GRÁFICAS=======================================================================
#===================================================================================INICIO APLICATIVO============================================================
if ativo:
    #Carregando Data Frame
    ativo = ativo + str(".SA")
    df = yf.download(ativo, period='180d')
    #Setup IFR2
    if Indicador == indicadores[1]:
        df['IFR2'] = ta.rsi(df['Close'],length=2)
        df['Highest'] = df['High'].rolling(2).max()
        df['Highest'] = df['Highest'].shift(1)
        #Definindo função para compras 
        def podeComprar(i,df):
            if (df['IFR2'][i] < 25.00):
                return True
            return False
          #Definindo função para vender
        def podeVender(i,df):
            if (df['Highest'][i] < df['Close'][i]):
                return True
            return False
        
        ativo = ativo.replace(".SA","")
        df['parametro'] = 25.00
        Operacoes(2,df)
        #Máxima dos 2 últimos dias
        #gráfico candlestick
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
        
        trace4 = {
            'x': df.index,
            'y':  df['Highest'],
            'type': 'scatter',
            'mode': 'lines',
            'line': {
                'width':1,
                'color': 'blue'
            },
            'name': 'Highest2'
        }
        #Sinal de Compra
        trace2 = {
            'x': df.index,
            'y': df['Buy'],
            'type': 'scatter',
            'mode':  'markers + text',
            'text': 'Buy',
            'line': {
                'width': 1,
                'color': 'white'
            },
            'name': 'Buy'
        }
        #Sinal de Venda
        trace3 = {
            'x': df.index,
            'y': df['Sell'],
            'type': 'scatter',
            'mode':  'markers + text',
            'text':'Sell',
            'line': {
                'width': 1,
                'color':'white'
            },
            'name': 'Sell'
        }
        #informar todos os dados e gráficos em uma lista
        data = [trace1, trace2, trace3, trace4]
        #configurar o layout do gráfico
        layout = go.Layout({
            'title': {
                'text': f'Gráfico3FR2 {ativo}',
                'font': {
                    'size': 20
                }
            }
        })
        #instanciar objeto Figure e plotar o gráfico
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig, width=800, height=800)
        #Indicador IFR2
       
       
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
                'width': 2,
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
        st.plotly_chart(fig_1,width=600, height=600)
 #===========================================================================================================================================================       
    #Média das 3 máximas e mínimas
    elif Indicador == indicadores[2]:
        df['Avg_Low3'] = df['Low'].rolling(3).mean()
        df['Avg_Low3'] = df['Avg_Low3'].shift(1)
        df['Avg_High3'] = df['High'].rolling(3).mean()
        df['Avg_High3'] = df['Avg_High3'].shift(1)
        def podeComprar(indice, dados):
            if (dados['Close'][indice] < dados['Avg_Low3'][indice]):
                return True
            return False
        #Definindo função para vender
        def podeVender(indice, dados):
            if (dados['Avg_High3'][indice] < dados['Close'][indice]):
                return True
            return False
        
        ativo = ativo.replace(".SA","")
        Operacoes(3,df)
        #gráfico candlestick
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
        #Mínima dos 3 ultimos dias
        trace4 = {
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
        #Máxima dos 3 últimos dias
        trace5 = {
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
        #Sinal de Compra
        trace4 = {
            'x': df.index,
            'y': df['Buy'],
            'type': 'scatter',
            'mode':  'markers + text',
            'text': 'Buy',
            'line': {
                'width': 1,
                'color': 'white'
            },
            'name': 'Buy'
        }
        #Sinal de Venda
        trace5 = {
            'x': df.index,
            'y': df['Sell'],
            'type': 'scatter',
            'mode':  'markers + text',
            'text':'Sell',
            'line': {
                'width': 1,
                'color':'white'
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
  #==============================================================================================================================================================
    #Setup Tutle 20-10
    elif Indicador == indicadores[3]:
            df['Highest 20'] = df['High'].rolling(20).max()
            df['Highest 20'] = df['Highest 20'].shift(1)
            df['Lowest 10'] = df['Low'].rolling(10).min()
            df['Lowest 10'] = df['Lowest 10'].shift(1)
            def podeComprar(indice, dados):
                if (dados['Highest 20'][indice] < dados['Close'][indice]):
                    return True
                return False
            #Definindo função para vender
            def podeVender(indice, dados):
                if (dados['Close'][indice] < dados['Lowest 10'][indice]):
                    return True
                return False
            
            ativo = ativo.replace(".SA","")
            Operacoes(20,df)
            #Gráfico candlestick
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
            #Mínima dos 10 últimos dias
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
            #Máxima dos 20 últimos dias
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
            #Sinal de Compra
            trace4 = {
                'x': df.index,
                'y': df['Buy'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Buy",
                'line': {
                    'width': 1,
                    'color': 'white'
                },
                'name': 'Buy'
            }
            #Sinal de Venda
            trace5 = {
                'x': df.index,
                'y': df['Sell'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Sell",
                'line': {
                    'width': 1,
                    'color': 'white'
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
    elif Indicador == indicadores[4]:
            #Média de 9.1
            df['avg_exp 9'] = df['Close'].ewm(span=9, min_periods=9).mean()
            df['avg_exp 9'] = df['avg_exp 9'].shift(1)
            def podeComprar(indice, dados):
                if (dados['Close'][indice] < dados['avg_exp 9'][indice]):
                    return True
                return False
            #Definindo função para vender
            def podeVender(indice, dados):
                if (dados['avg_exp 9'][indice] < dados['Close'][indice]):
                    return True
                return False
            
            ativo = ativo.replace(".SA","")
            Operacoes(9,df)
        
            #Gráfico candlestick
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
            # média exponecial dos últimos 9 dias
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
            #Sinal de Compra
            trace3 = {
                'x': df.index,
                'y': df['Buy'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Buy",
                'line': {
                    'width': 1,
                    'color': 'white'
                },
                'name': 'Buy'
            }
            #Sinal de Venda
            trace4 = {
                'x': df.index,
                'y': df['Sell'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Sell",
                'line': {
                    'width': 1,
                    'color': 'white'
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
  
    
    #SuperTrend
    elif Indicador == indicadores[5]:
            #Cálculo do indicador SuperTrend
           
            df['L'] = ta.supertrend(df['High'],df['Low'],df['Close'],10,3)["SUPERTl_10_3.0"]
            df['S'] = ta.supertrend(df['High'],df['Low'],df['Close'],10,3)["SUPERTs_10_3.0"]
            def podeComprar(i,dados):
                if (dados['S'] [i-1]<dados['Close'][i]):
                    return True
                return False
            #Definindo função para vender
            def podeVender(i,dados):
                if (dados['Close'][i] < dados['L'][i-1]):
                    return True
                return False
           
            ativo = ativo.replace(".SA","")
            Operacoes(12,df)
           
            # gráfico candlestick
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
            # SuperTrend Inferior
            trace2 = {
                'x': df.index,
                'y': df['L'],
                'type': 'scatter',
                'mode': 'lines',
                'line': {
                    'width': 2,
                    'color': 'blue'
                },
                'name': 'SUPERTREND DOWN'
            }
            
            # SuperTrend Superior
            trace3 = {
                'x': df.index,
                'y': df['S'],
                'type': 'scatter',
                'mode': 'lines',
                'line': {
                    'width': 2,
                    'color': 'yellow'
                },
                'name': 'SUPERTREND UPPER'
            }
            # Sinal de Compra
            trace4 = {
                'x': df.index,
                'y': df['Buy'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text': "Buy",
                'line': {
                    'width': 1,
                    'color': 'white'

                },
                'name': 'Buy'
            }
            # Sinal de Venda
            trace5 = {
                'x': df.index,
                'y': df['Sell'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Sell",
                'line': {
                    'width': 1,
                    'color': 'white'
                },
                'name': 'Sell'
            }
            # informar todos os dados e gráficos em uma lista
            data = [trace1, trace2, trace3, trace4,trace5]
            # configurar o layout do gráfico
            layout = go.Layout({
                'title': {
                    'text': f'Gráfico SuperTrend {ativo}',
                    'font': {
                        'size': 20
                    }
                }
            })
            # instanciar objeto Figure e plotar o gráfico
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, width=600, height=600)
    elif Indicador == indicadores[6]:
            df['Highest 20'] = df['High'].rolling(10).max()
            df['Highest 20'] = df['Highest 20'].shift(1)
            df['Lowest 10'] = df['Low'].rolling(10).min()
            df['Lowest 10'] = df['Lowest 10'].shift(1)
            def podeComprar(indice, dados):
                if (dados['Highest 20'][indice] < dados['Close'][indice]):
                    return True
                return False
            #Definindo função para vender
            def podeVender(indice, dados):
                if (dados['Close'][indice] < dados['Lowest 10'][indice]):
                    return True
                return False
            
            ativo = ativo.replace(".SA","")
            Operacoes(10,df)
            #Gráfico candlestick
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
            #Mínima dos 10 últimos dias
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
            #Máxima dos 20 últimos dias
            trace3 = {
                'x': df.index,
                'y': df['Highest 20'],
                'type': 'scatter',
                'mode': 'lines',
                'line': {
                    'width': 1,
                    'color': 'yellow'
                },
                'name': 'Highest 10'
            }
            #Sinal de Compra
            trace4 = {
                'x': df.index,
                'y': df['Buy'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Buy",
                'line': {
                    'width': 1,
                    'color': 'white'
                },
                'name': 'Buy'
            }
            #Sinal de Venda
            trace5 = {
                'x': df.index,
                'y': df['Sell'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Sell",
                'line': {
                    'width': 1,
                    'color': 'white'
                },
                'name': 'Sell'
            }
            # informar todos os dados e gráficos em uma lista
            data = [trace1, trace2, trace3, trace4, trace5]
            # configurar o layout do gráfico
            layout = go.Layout({
                'title': {
                    'text': f'Gráfico Dochian 10/10 {ativo}',
                    'font': {
                        'size': 20
                    }
                }
            })
            # instanciar objeto Figure e plotar o gráfico
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, width=300, height=300)
           
    else:
            df['Standard Deviation'] = df['Close'].rolling(20).std()
            df['Middle Band'] = df['Adj Close'].rolling(20).mean()
            df['Upper Band'] = df['Middle Band'] + df['Standard Deviation'] * 2.00
            df['Lower Band'] = df['Middle Band'] - df['Standard Deviation'] * 2.00
            def podeComprar(indice, dados):
                if (dados['Close'][indice]< df['Lower Band'][indice-1]):
                    return True
                return False
            #Definindo função para vender
            def podeVender(indice, dados):
                if (df['Lower Band'][indice-1] < dados['Close'][indice]):
                    return True
                return False
            
            ativo = ativo.replace(".SA","")
            Operacoes(10,df)
            #Gráfico candlestick
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
            #Mínima dos 10 últimos dias
            trace2 = {
                'x': df.index,
                'y': df['Lower Band'],
                'type': 'scatter',
                'mode': 'lines',
                'line': {
                    'width': 1,
                    'color': 'blue'
                },
                'name': 'Banda Upper'
            }
           
            #Sinal de Compra
            trace3 = {
                'x': df.index,
                'y': df['Buy'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Buy",
                'line': {
                    'width': 1,
                    'color': 'white'
                },
                'name': 'Buy'
            }
            #Sinal de Venda
            trace4 = {
                'x': df.index,
                'y': df['Sell'],
                'type': 'scatter',
                'mode': 'markers + text',
                'text':"Sell",
                'line': {
                    'width': 1,
                    'color': 'white'
                },
                'name': 'Sell'
            }
            # informar todos os dados e gráficos em uma lista
            data = [trace1, trace2, trace3, trace4]
            # configurar o layout do gráfico
            layout = go.Layout({
                'title': {
                    'text': f'Gráfico Bandas de Bollinger {ativo}',
                    'font': {
                        'size': 20
                    }
                }
            })
            # instanciar objeto Figure e plotar o gráfico
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, width=300, height=300)
            
            
    
    
