import pandas as pd
import numpy as np
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots


# Graficar para poner n lineas de una moneda
def line_chart(coin: str, variable: str, data: pd.DataFrame):
    # Cambiar formato de pandas para no tener errores
    pd.options.mode.chained_assignment = None

    # Seleccionar solo la data de la moneda que necesitamos
    data_coin = data[data["coin"] == coin]
    # Obtener dia de operacion
    day = data_coin.iloc[0, 0][0:10]
    # Obtener set de mercado
    market = list(set(data["exchange"]))

    # Hacer temp con informacion de cada mercado y su fecha
    temp = pd.DataFrame(data_coin[data_coin["exchange"] == market[0]]["timeStamp"])
    temp["timeStamp"] = [i[12:] for i in temp["timeStamp"]]

    for mk in market:
        temp[f"{variable}_{mk}"] = data_coin[data_coin["exchange"] == mk][variable].values

    # Graficar
    fig = px.line(temp, x='timeStamp', y=temp.columns[1:])
    fig.update_layout(title=f"{variable} {coin}", xaxis_title=f"timeStamp ({day})", yaxis_title=f"{variable}")

    # Mostrar figuras
    fig.show()


# Grafica de total volume de n exchanges
def total_volume_chart(coin: str, data: pd.DataFrame):
    # Siempre sera total volume
    variable = "total_volume"
    # Cambiar formato de pandas para no tener errores
    pd.options.mode.chained_assignment = None  # default='warn'
    # Seleccionar solo la data de la moneda que necesitamos
    data_coin = data[data["coin"] == coin]
    # Obtener dia de operacion
    day = data_coin.iloc[0, 0][0:10]
    # Obtener set de mercado
    market = list(set(data["exchange"]))

    # Hacer temp con informacion de cada mercado y su fecha
    temp = pd.DataFrame(data_coin[data_coin["exchange"] == market[0]]["timeStamp"])
    temp["timeStamp"] = [i[12:] for i in temp["timeStamp"]]

    # Estandarizar fechas
    lista = []
    for i in range(len(market)):
        lista.append([i for i in temp.values])
    l = list(temp["timeStamp"].values)
    k = l
    for i in range(len(market) - 1):
        l = l + k
    data_coin["timeStamp"] = l

    # Graficar
    fig = px.line(data_coin, x='timeStamp', y=data_coin[variable], facet_col="exchange")
    fig.update_layout(title=f"{variable} {coin}", xaxis_title=f"timeStamp ({day})", yaxis_title=variable)
    fig.update_traces(line_color='black')

    # Mostrar grafica
    fig.show()


# Histograma de Ask y Bids
def ask_bid_histograms(coin: str, data: pd.DataFrame):
    # Cambiar formato de pandas para no tener errores
    pd.options.mode.chained_assignment = None  # default='warn'
    # Seleccionar solo la data de la moneda que necesitamos
    data_coin = data[data["coin"] == coin]
    # Obtener dia de operacion
    day = data_coin.iloc[0, 0][0:10]
    # Obtener set de mercado
    market = list(set(data["exchange"]))

    # Hacer temp con informacion de cada mercado y su fecha
    temp = pd.DataFrame(data_coin[data_coin["exchange"] == market[0]]["timeStamp"])
    temp["timeStamp"] = [i[12:] for i in temp["timeStamp"]]

    # Estandarizar fechas
    lista = []
    for i in range(len(market)):
        lista.append([i for i in temp.values])
    l = list(temp["timeStamp"].values)
    k = l
    for i in range(len(market) - 1):
        l = l + k
    data_coin["timeStamp"] = l

    # Grafica 1 Ask
    fig = px.histogram(data_coin, x='timeStamp', y=data_coin["ask_volume"], facet_col="exchange")
    fig.update_layout(title=f"ask volume {coin}", xaxis_title=f"timeStamp ({day})", yaxis_title="ask_volume")
    # Grafica 2. Bid
    fig2 = px.histogram(data_coin, x='timeStamp', y=data_coin["bid_volume"], facet_col="exchange")
    fig2.update_layout(title=f"bid volume {coin}", xaxis_title=f"timeStamp ({day})", yaxis_title="bid_volume")

    # Mostrar graficas
    fig.show(), fig2.show()


# Grafica de subplots de niveles por mercado segun una moneda
def levels_markets(coin: str, data: pd.DataFrame):
    # Obtener data de la moneda a graficar
    data_coin = data[data["coin"]==coin]
    # Obtener set de mercado
    market=list(set(data["exchange"]))

    # Inicializar figura
    fig = make_subplots(rows=1, cols=3,
                        shared_yaxes=True,
                        subplot_titles = (f"Levels {market[0]} {coin}", f"Levels {market[1]} {coin}", f"Levels {market[2]} {coin}"))

    # Figura 1 BID Y ASK
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[0]]["ask"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[0]]["ask_volume"],
        orientation='h',
        marker_color="black",
        name=f"ask {market[0]}"),
        row=1, col=1)
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[0]]["bid"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[0]]["bid_volume"],
        orientation='h', name=f"bid {market[0]}",
        marker_color="salmon"),
        row=1, col=1
    )

    # Figura 2 BID Y ASK
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[1]]["ask"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[1]]["ask_volume"],
        orientation='h', marker_color="blue", name=f"ask {market[1]}",),
        row=1, col=2)
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[1]]["bid"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[1]]["bid_volume"],
        orientation='h', name=f"bid {market[1]}",
        marker_color="green"),
        row=1, col=2
    )

    # Figura 3 BID Y ASK
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[2]]["ask"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[2]]["ask_volume"],
        orientation='h', marker_color="navy", name=f"ask {market[2]}",),
        row=1, col=3)
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[2]]["bid"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[2]]["bid_volume"],
        orientation='h', name=f"bid {market[2]}",
        marker_color="red"),
        row=1, col=3
    )

    # Mostrar figura
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_xaxes(title_text="Volume")
    fig.show()