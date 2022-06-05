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

def Trace_1(df,ativo):
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
    return trace1

def Trace_2(df):
#Sinal de Compra
    trace3 = {
            'x': df.index,
            'y': df['Buy'],
            'type': 'scatter',
            'mode': 'markers + text',
            'text': "Buy",
            'line': {
                'width':1,
                'color': 'white'
            },
            'name': 'Buy'
        }
    return trace3

def Trace_4(df):
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
    return trace4

