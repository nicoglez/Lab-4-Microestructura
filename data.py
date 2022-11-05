import ccxt
import pandas as pd

from functions import ccxt_getter
from functions import pd_to_dict

# Definir diccionario con mercados de donde descarga la info y sus metodos para descargar
markets = {"kraken": ccxt.kraken(), "currencycom": ccxt.currencycom(), "binance": ccxt.binance()}
# Definir las monedas y sus cambios a bajar
coins = ['BTC/USDT', 'BTC/EUR', "ETH/USDT"]

# Descargar la base de datos en un xlsx, si se quiere testear la funcion se puede correr menos veces minutes_fetch
#ccxt_getter(markets=markets, coins=coins, minutes_fetch=120, filepath="files/data.xlsx")

# Leer xlsx generado
data = pd.read_excel("files/data_Lab_4.xlsx", engine='openpyxl').sort_values(by="timeStamp")
data_dict = pd_to_dict(data)
