import pandas as pd
import numpy as np
import warnings
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
    # Obtener data de la moneda a graficar
    data_coin = data[data["coin"]==coin]
    # Obtener set de mercado
    market = list(set(data["exchange"]))

    # Obtener dia de operacion
    day = data_coin.iloc[0,0][0:10]

    # Hacer temp con informacion de cada mercado y su fecha
    data_coin["timeStamp"] = [i[12:] for i in data_coin["timeStamp"]]

    # Inicializar figura
    fig = make_subplots(rows=1, cols=3,
                        shared_yaxes=True,
                        subplot_titles = (f"{market[0]}",
                                          f"{market[1]}",
                                          f"{market[2]}"))

    # Figura 1
    fig.add_trace(go.Bar(
        y= data_coin[data_coin["exchange"]==market[0]]["total_volume"],
        x= data_coin[data_coin["exchange"]==market[0]]["timeStamp"],
        marker_color="black", width = 2,
        name=f"total_volume {market[0]}"),
        row=1, col=1)

    # Figura 2
    fig.add_trace(go.Bar(
        y= data_coin[data_coin["exchange"]==market[1]]["total_volume"],
        x= data_coin[data_coin["exchange"]==market[0]]["timeStamp"],
        marker_color="red", width = 2,
        name=f"tota_volume {market[1]}",),
        row=1, col=2)

    # Figura 3
    fig.add_trace(go.Bar(
        y= data_coin[data_coin["exchange"]==market[2]]["total_volume"],
        x= data_coin[data_coin["exchange"]==market[0]]["timeStamp"],
        marker_color="navy", width = 2,
        name=f"total_volume {market[2]}",),
        row=1, col=3)

    # Mostrar figura
    fig.update_layout(title_text=f"Total Volume {coin}")
    fig.update_yaxes(title_text="Total Volume", row=1, col=1)
    fig.update_xaxes(title_text=f"Time Stamp ({day})")
    fig.show()


# Grafica de subplots de niveles por mercado segun una moneda
def ask_bid_volume(coin: str, data: pd.DataFrame):
    # Obtener data de la moneda a graficar
    data_coin = data[data["coin"] == coin]

    # Obtener set de mercado
    market = list(set(data["exchange"]))

    # Obtener dia de operacion
    day = data_coin.iloc[0, 0][0:10]

    # Hacer temp con informacion de cada mercado y su fecha
    data_coin["timeStamp"] = [i[12:] for i in data_coin["timeStamp"]]

    # Inicializar figura
    fig = make_subplots(rows=2, cols=3,
                        shared_yaxes=True,
                        subplot_titles=(f"ask {market[0]}",
                                        f"ask {market[1]}",
                                        f"ask {market[2]}",
                                        f"bid {market[0]}",
                                        f"bid {market[1]}",
                                        f"bid {market[2]}"))

    # Figura 1 BID Y ASK
    fig.add_trace(go.Bar(
        y=data_coin[data_coin["exchange"] == market[0]]["ask_volume"],
        x=data_coin[data_coin["exchange"] == market[0]]["timeStamp"],
        marker_color="navy", width=3,
        name=f"ask {market[0]}"),
        row=1, col=1)

    fig.add_trace(go.Bar(
        y=data_coin[data_coin["exchange"] == market[0]]["bid_volume"],
        x=data_coin[data_coin["exchange"] == market[0]]["timeStamp"],
        name=f"bid {market[0]}", width=3,
        marker_color="green"),
        row=2, col=1
    )

    # Figura 2 BID Y ASK
    fig.add_trace(go.Bar(
        y=data_coin[data_coin["exchange"] == market[1]]["ask_volume"],
        x=data_coin[data_coin["exchange"] == market[0]]["timeStamp"],
        marker_color="navy", width=5,
        name=f"ask {market[1]}"),
        row=1, col=2)
    fig.add_trace(go.Bar(
        y=data_coin[data_coin["exchange"] == market[1]]["bid_volume"],
        x=data_coin[data_coin["exchange"] == market[0]]["timeStamp"],
        name=f"bid {market[1]}", width=5,
        marker_color="green"),
        row=2, col=2
    )

    # Figura 3 BID Y ASK
    fig.add_trace(go.Bar(
        y=data_coin[data_coin["exchange"] == market[2]]["ask_volume"],
        x=data_coin[data_coin["exchange"] == market[0]]["timeStamp"],
        marker_color="navy", width=3,
        name=f"ask {market[2]}", ),
        row=1, col=3)
    fig.add_trace(go.Bar(
        y=data_coin[data_coin["exchange"] == market[2]]["bid_volume"],
        x=data_coin[data_coin["exchange"] == market[0]]["timeStamp"],
        name=f"bid {market[2]}",
        marker_color="green", width=3),
        row=2, col=3
    )

    # Mostrar figura
    fig.update_yaxes(title_text="Volume", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_xaxes(title_text=f"Time Stamp ({day})")
    fig.update_layout(title_text=f"Bid & Ask Volume {coin}", width=1000, height=800)
    fig.show()


# Grafica de subplots de niveles por mercado segun una moneda
def levels_markets(coin: str, data: pd.DataFrame):
    # Obtener data de la moneda a graficar
    data_coin = data[data["coin"]==coin]
    # Obtener set de mercado
    market=list(set(data["exchange"]))

    # Inicializar figura
    fig = make_subplots(rows=1, cols=3,
                        shared_yaxes=True,
                        subplot_titles = (f"{market[0]}",
                                          f"{market[1]}",
                                          f"{market[2]}"))

    # Figura 1 BID Y ASK
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[0]]["ask"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[0]]["ask_volume"],
        orientation='h', width=3,
        marker_color="navy",
        name=f"ask {market[0]}"),
        row=1, col=1)
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[0]]["bid"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[0]]["bid_volume"],
        orientation='h', width=3,
        name=f"bid {market[0]}",
        marker_color="red"),
        row=1, col=1
    )

    # Figura 2 BID Y ASK
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[1]]["ask"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[1]]["ask_volume"],
        orientation='h', width=3,
        marker_color="navy",
        name=f"ask {market[1]}",),
        row=1, col=2)
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[1]]["bid"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[1]]["bid_volume"],
        orientation='h', width=3,
        name=f"bid {market[1]}",
        marker_color="red"),
        row=1, col=2
    )

    # Figura 3 BID Y ASK
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[2]]["ask"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[2]]["ask_volume"],
        orientation='h', width=3,
        marker_color="navy",
        name=f"ask {market[2]}",),
        row=1, col=3)
    fig.add_trace(go.Bar(
        y= np.array(sorted(data_coin[data_coin["exchange"]==market[2]]["bid"])).astype(str),
        x= data_coin[data_coin["exchange"]==market[2]]["bid_volume"],
        orientation='h', width=3,
        name=f"bid {market[2]}",
        marker_color="red"),
        row=1, col=3
    )

    # Mostrar figura
    fig.update_layout(title_text=f"Levels {coin}")
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_xaxes(title_text="Volume")
    fig.show()


# Funcion para graficar roll spread
def roll_spread_plot(roll_data: pd.DataFrame):
    # Ignorar errores de deprecation
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Obtener set de mercado
    market = ["binance", "currencycom", "kraken"]
    coin = ['BTC/USDT', 'BTC/EUR', "ETH/USDT"]

    # Obtener dia de operacion
    day = roll_data.iloc[0, 0][0:10]
    # Hacer temp con informacion de cada mercado y su fecha
    roll_data["timeStamp"] = [i[12:] for i in roll_data["timeStamp"]]

    # Inicializar figura
    fig = make_subplots(rows=1, cols=3,
                        shared_yaxes=True,
                        subplot_titles=(f"{coin[0]}",
                                        f"{coin[1]}",
                                        f"{coin[2]}"))

    # Figura 1
    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[0]) & (roll_data["coin"] == coin[0])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[0])]["timeStamp"],
        marker_color="black",
        name=f"effective spread {market[0]}"),
        row=1, col=1)

    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[0])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[0])]["timeStamp"],
        marker_color="red",
        name=f"effective spread {market[1]}"),
        row=1, col=1)

    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[2]) & (roll_data["coin"] == coin[0])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[0])]["timeStamp"],
        marker_color="blue",
        name=f"effective spread {market[2]}"),
        row=1, col=1)

    # Figura 2
    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[0]) & (roll_data["coin"] == coin[1])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[1])]["timeStamp"],
        marker_color="black",
        showlegend=False),
        row=1, col=2)

    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[1])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[1])]["timeStamp"],
        marker_color="red",
        showlegend=False),
        row=1, col=2)

    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[2]) & (roll_data["coin"] == coin[1])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[1])]["timeStamp"],
        marker_color="blue",
        showlegend=False),
        row=1, col=2)

    # Figura 3
    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[0]) & (roll_data["coin"] == coin[2])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[2])]["timeStamp"],
        marker_color="black",
        showlegend=False),
        row=1, col=3)

    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[2])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[2])]["timeStamp"],
        marker_color="red",
        showlegend=False),
        row=1, col=3)

    fig.add_trace(go.Line(  # Usaremos un promedio movil con ventana de 20 dias debido a que si no parece ruido blanco
        y=roll_data[(roll_data["exchange"] == market[2]) & (roll_data["coin"] == coin[2])]["effective spread"].rolling(
            20).mean().dropna(),
        x=roll_data[(roll_data["exchange"] == market[1]) & (roll_data["coin"] == coin[2])]["timeStamp"],
        marker_color="blue",
        showlegend=False),
        row=1, col=3)

    # Mostrar figura
    fig.update_layout(title_text="Effective Spread - Roll Model")
    fig.update_yaxes(title_text="Effective Spread", row=1, col=1)
    fig.update_xaxes(title_text=f"Time Stamp ({day})")
    fig.show()
