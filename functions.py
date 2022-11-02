import numpy as np
import pandas as pd
from time import sleep
import datetime
import ccxt


# Funcion para bajar de la libreria ccxt la informacion de x monedas de x mercados a un xlsx
def ccxt_getter(markets: dict, coins: list, minutes_fetch: int, filepath=str):
    # Funcion que baja la informacion
    def itter_tool(markets, coins, data_f):
        # ID para las Rows
        ID = 0
        # Construccion de data frame
        data = pd.DataFrame(index=["exchange", "coin", "timeStamp", "level", "ask", "ask_volume", "bid", "bid_volume",
                                   "spread", "total_volume", "mid_price", "open_price", "high_price", "low_price",
                                   "close_price", "vwap"])
        # Iterar por cada moneda
        for coin in coins:
            # Iterar por cada mercado
            for market in markets.keys():

                # Intentar bajar la informacion de la API, a veces falla
                try:
                    ID += 1
                    # Obtener metodo de libreria segun el x mercado
                    method = markets.get(market)
                    # Definir exchange como str
                    exchange = market
                    # definir time samp de metodo
                    time_samp = method.iso8601(method.milliseconds())
                    # sacar time stamp
                    time_stamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    # Obtener libro de ordenes
                    order_book = method.fetch_order_book(coin)

                    # Obtener caracteristicas del libro de ordenes
                    ask_data = pd.DataFrame(order_book['asks'])
                    bid_data = pd.DataFrame(order_book['bids'])
                    bid = order_book['bids'][0][0] if len(order_book['bids']) > 0 else None
                    bid_volume = order_book['bids'][0][1] if len(order_book['bids']) > 0 else None
                    ask = order_book['asks'][0][0] if len(order_book['asks']) > 0 else None
                    ask_volume = order_book['asks'][0][1] if len(order_book['asks']) > 0 else None
                    total_volume = ask_volume + bid_volume
                    level = len(bid_data) + len(ask_data)
                    spread = (ask - bid) if (bid and ask) else None
                    mid_price = (ask + bid) / 2
                    open_price = method.fetch_ohlcv(coin, "1m", limit=1)[-1][1]
                    high_price = method.fetch_ohlcv(coin, "1m", limit=1)[-1][2]
                    low_price = method.fetch_ohlcv(coin, "1m", limit=1)[-1][3]
                    close_price = method.fetch_ohlcv(coin, "1m", limit=1)[-1][4]
                    vwap = ask * (ask_volume / total_volume) + bid * (bid_volume / total_volume)

                # En caso de que falle la API, asumiremos que la data no ha cambiado, agarrando el dato mas reciente de la
                # misma moneda para el caso anterior en el mismo mercado
                except:
                    case = data_f.iloc[:, len(data_f.T) - len(markets) * len(coins)]
                    exchange = market
                    coin = case.coin
                    time_stamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    level = case.level
                    ask = case.ask
                    ask_volume = case.ask_volume
                    bid = case.bid
                    bid_volume = case.bid_volume
                    spread = case.spread
                    total_volume = case.total_volume
                    mid_price = case.mid_price
                    open_price = case.open_price
                    high_price = case.high_price
                    low_price = case.low_price
                    close_price = case.close_price
                    vwap = case.vwap
                # Llenar data
                data[ID] = [exchange, coin, time_stamp, level, ask, ask_volume, bid, bid_volume, spread,
                            total_volume, mid_price, open_price, high_price, low_price, close_price, vwap]
        # Regresar data
        return data

    # Crear data frame
    data = pd.DataFrame(index=["exchange", "coin", "timeStamp", "level", "ask", "ask_volume", "bid", "bid_volume",
                               "spread", "total_volume", "mid_price", "open_price", "high_price", "low_price",
                               "close_price", "vwap"])

    # For que llama n observaciones la funcion anterior
    for i in range(minutes_fetch):
        # Appendear data n veces
        data = data.T.append(itter_tool(markets, coins, data).T).T
        # Esperar proceso 60 segundos
        sleep(60)

    # Sobre escribir en xlsx
    data.T.set_index("timeStamp").to_excel(filepath)
    print("Archivo", filepath, "importado correctamente a Excel")
    # return data.T.set_index(np.arange(0, len(data.T)))


# Funcion para convertir Data Frame a Diccionario
def pd_to_dict(data: pd.DataFrame) -> dict:
    # Dic vacio
    final = {}

    # Iterar por cada mercado
    for market in set(data["exchange"]):

        # Fitrar por cada bolsa
        temp_data = data[data["exchange"] == market]
        temp_data.set_index(np.arange(0, len(temp_data)), inplace=True)

        # Diccionario vacio
        temp_dict = {}
        # Iterar para sacar la informacion por mercado
        for i in range(len(temp_data)):
            temp_ocurrencias = {
                temp_data["timeStamp"][i]: {
                    "Cripto": temp_data["coin"][i],
                    "level": temp_data["level"][i],
                    "ask": temp_data["ask"][i],
                    "bid": temp_data["bid"][i],
                    "ask_volume": temp_data["ask_volume"][i],
                    "bid_volume": temp_data["bid_volume"][i],
                    "total_volume": temp_data["total_volume"][i],
                    "mid_price": temp_data["mid_price"][i],
                    "vwap": temp_data["vwap"][i],
                    "spread": temp_data["spread"][i],
                    "open_price": temp_data["open_price"][i],
                    "low_price": temp_data["low_price"][i],
                    "high_price": temp_data["high_price"][i],
                    "close_price": temp_data["close_price"][i],
                }
            }

            temp_dict.update(temp_ocurrencias)

        final.update({market: temp_dict})

    # Regresar diccionario
    return final

