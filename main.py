# Importacion de datos
from data import data, data_dict
# Importar funciones de graficos
import visualizations as vst
# Importar funcion para hacer roll model
from functions import roll_model


# Parte 1. Datos descargados de API de criptos (dict y df)
print("El tamaño de nuestra información es de", len(data),"observaciones")
display(data.head(3))
display(data.tail(3))
display(data_dict)

# Parte 2. Analisis de microestructura con graficas
# BTC/USDT
vst.line_chart("BTC/USDT", "mid_price", data)
vst.line_chart("BTC/USDT", "vwap", data)
vst.line_chart("BTC/USDT", "spread", data)
vst.total_volume_chart("BTC/USDT", data)
vst.ask_bid_volume("BTC/USDT", data)
vst.levels_markets("BTC/USDT", data)
# BTC/EUR
vst.line_chart("BTC/EUR", "mid_price", data)
vst.line_chart("BTC/EUR", "vwap", data)
vst.line_chart("BTC/EUR", "spread", data)
vst.total_volume_chart("BTC/EUR", data)
vst.ask_bid_volume("BTC/EUR", data)
vst.levels_markets("BTC/EUR", data)
# ETH/USDT
vst.line_chart("ETH/USDT", "mid_price", data)
vst.line_chart("ETH/USDT", "vwap", data)
vst.line_chart("ETH/USDT", "spread", data)
vst.total_volume_chart("ETH/USDT", data)
vst.ask_bid_volume("ETH/USDT", data)
vst.levels_markets("ETH/USDT", data)

# Parte 3. Modelado de la Microestructura
# Crear dataframe con spread de roll
roll_data = roll_model(data=data, rezagos=5)
# Visualizar roll spread
vst.roll_spread_plot(roll_data)
