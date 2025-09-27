import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import os

# --- Configuración de Seguridad y Entorno ---
API_KEY = os.environ.get('BINANCE_API_KEY', '') 
API_SECRET = os.environ.get('BINANCE_API_SECRET', '')

# --- Constantes del Requerimiento ---
ASSETS = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT']
TIMEFRAME = Client.KLINE_INTERVAL_1DAY 
START_DATE = '2021-01-01' 

# --- NUEVO ARREGLO: Ruta de Exportación ---
# La carpeta se creará en el mismo directorio donde ejecutas el script.
OUTPUT_DIR = 'datos_binance' 

# Función para obtener la fecha de ayer
def get_yesterday_date():
    """Calcula y devuelve la fecha de ayer como string 'YYYY-MM-DD'."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

END_DATE = get_yesterday_date() 


# --- Función Principal de Extracción de Datos ---
def get_crypto_data(symbol: str, interval: str, start_str: str, end_str: str, output_path: str):
    """
    Extrae datos históricos de la API de futuros de Binance y los exporta a un CSV
    en la ruta especificada.
    
    Args:
        symbol (str): Ticker del activo.
        interval (str): Timeframe.
        start_str (str): Fecha de inicio.
        end_str (str): Fecha de fin.
        output_path (str): Directorio donde se guardará el CSV.
        
    Returns:
        pd.DataFrame: DataFrame de pandas con los datos o None.
    """
    # Inicializar el cliente
    client = Client(API_KEY, API_SECRET)

    print(f"-> Extrayendo datos para {symbol} desde {start_str} hasta {end_str}...")

    try:
        # Usamos futures_historical_klines que maneja la paginación.
        klines = client.futures_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_str,
            end_str=end_str 
        )

    except Exception as e:
        print(f"Error al obtener datos de la API para {symbol}: {e}")
        return None

    # Columnas esperadas de la API
    cols = [
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
        'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
        'Taker Buy Quote Asset Volume', 'Ignore'
    ]

    df = pd.DataFrame(klines, columns=cols)

    # --- Procesamiento de Datos ---
    df = df[['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
    df.drop('Open Time', axis=1, inplace=True)
    df.set_index('Date', inplace=True)

    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    # 6. Exportar a CSV en la RUTA ESPECIFICADA
    filename = f"{symbol}.csv"
    full_path = os.path.join(output_path, filename)
    
    df.to_csv(full_path)
    print(f"-> Datos de {symbol} guardados exitosamente en: {full_path}. Filas: {len(df)}")

    return df


# --- Ejecución Principal del Script ---
if __name__ == '__main__':
    print("--- Inicio de Extracción de Datos de Mercado de Binance ---")
    
    # 1. Crear el directorio de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Directorio de salida creado: {OUTPUT_DIR}")
        
    print(f"Rango de Fechas: {START_DATE} a {END_DATE} (Timeframe: 1 Day)")
    print("-" * 50)

    for asset in ASSETS:
        # 2. Pasar la ruta de salida a la función
        get_crypto_data(
            symbol=asset,
            interval=TIMEFRAME,
            start_str=START_DATE,
            end_str=END_DATE,
            output_path=OUTPUT_DIR
        )
        print("-" * 50)

    print("Data extraction finished :)")
