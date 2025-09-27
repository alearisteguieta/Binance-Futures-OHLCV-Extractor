#!/usr/bin/env python3
"""
Binance Crypto Data Extractor
Extrae datos históricos de mercado (candlestick) desde la API de Binance
y los exporta a archivos CSV individuales para cada activo.
"""

import os
import pandas as pd
import requests
from datetime import datetime, timezone, timedelta

def criptodata(symbol):
    """
    Extrae datos históricos de candlestick para un símbolo específico desde Binance
    
    Args:
        symbol (str): Símbolo del activo (ej. 'BTCUSDT')
    
    Returns:
        pandas.DataFrame: DataFrame con los datos históricos procesados
    """
    
    # URL base de la API pública de Binance (no requiere autenticación para datos históricos)
    base_url = "https://api.binance.com"
    
    # Definir fechas de inicio y fin
    start_date = datetime(2021, 1, 1, tzinfo=timezone.utc)
    end_date = datetime.now(timezone.utc) - timedelta(days=1)  # Día anterior
    
    print(f"📈 Extrayendo datos para {symbol} desde {start_date.strftime('%Y-%m-%d')} hasta {end_date.strftime('%Y-%m-%d')}")
    
    try:
        # Convertir fechas a timestamps en milisegundos (formato requerido por Binance)
        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)
        
        # Obtener datos de candlestick históricos usando requests
        # Endpoint de Binance para klines (datos de candlestick)
        endpoint = f"{base_url}/api/v3/klines"
        
        # Parámetros para la consulta
        params = {
            'symbol': symbol,
            'interval': '1d',  # Timeframe diario
            'startTime': start_timestamp,
            'endTime': end_timestamp,
            'limit': 1000  # Máximo por request
        }
        
        # Realizar petición a la API
        response = requests.get(endpoint, params=params)
        
        # Verificar si la petición fue exitosa
        if response.status_code != 200:
            print(f"❌ Error en la API: {response.status_code} - {response.text}")
            return None
        
        # Obtener los datos JSON
        klines = response.json()
        
        # Verificar si se obtuvieron datos
        if not klines:
            print(f"❌ No se encontraron datos para {symbol}")
            return None
        
        # Crear DataFrame con los datos obtenidos
        # Estructura de klines: [timestamp, open, high, low, close, volume, close_time, ...]
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Seleccionar solo las columnas necesarias
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
        # Convertir timestamp a fecha legible
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
        
        # Renombrar columnas según requerimientos
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Convertir valores numéricos (vienen como strings desde la API)
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df[numeric_columns] = df[numeric_columns].astype(float)
        
        # Establecer la fecha como índice
        df.set_index('Date', inplace=True)
        
        # Ordenar por fecha (más antigua primero)
        df.sort_index(inplace=True)
        
        # Exportar a CSV
        filename = f"{symbol}.csv"
        full_path = os.path.abspath(filename)
        df.to_csv(filename)
        
        print(f"✅ Datos exportados exitosamente a:")
        print(f"   📁 Ruta completa: {full_path}")
        print(f"   Registros: {len(df)}")
        print(f"   Rango: {df.index.min().strftime('%Y-%m-%d')} a {df.index.max().strftime('%Y-%m-%d')}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error al procesar {symbol}: {str(e)}")
        return None

def main():
    """
    Función principal que procesa todos los activos especificados
    """
    
    print("🚀 Iniciando extracción de datos de Binance")
    print("=" * 50)
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    print(f"📄 Archivos CSV se guardarán en: {os.path.abspath('.')}")
    print("=" * 50)
    
    # Lista de activos a procesar
    assets = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT']
    
    successful_extractions = []
    failed_extractions = []
    
    # Procesar cada activo
    for asset in assets:
        print(f"\n📊 Procesando {asset}...")
        
        try:
            df = criptodata(asset)
            if df is not None:
                successful_extractions.append(asset)
            else:
                failed_extractions.append(asset)
        except Exception as e:
            print(f"❌ Error inesperado procesando {asset}: {str(e)}")
            failed_extractions.append(asset)
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📈 RESUMEN DE EXTRACCIÓN")
    print("=" * 50)
    
    if successful_extractions:
        print(f"✅ Extracciones exitosas ({len(successful_extractions)}):")
        for asset in successful_extractions:
            full_path = os.path.abspath(f"{asset}.csv")
            print(f"   • {asset}.csv")
            print(f"     📁 {full_path}")
            print()
    
    if failed_extractions:
        print(f"❌ Extracciones fallidas ({len(failed_extractions)}):")
        for asset in failed_extractions:
            print(f"   • {asset}")
    
    print(f"\nTotal procesados: {len(assets)}")
    print(f"Exitosos: {len(successful_extractions)}")
    print(f"Fallidos: {len(failed_extractions)}")
    
    print("\n🎉 Data extraction finished :)")

if __name__ == "__main__":
    # Verificar dependencias
    try:
        import requests
        import pandas as pd
    except ImportError as e:
        print(f"❌ Error: Falta instalar dependencias: {e}")
        print("   Instala con: pip install requests pandas")
        exit(1)
    
    # Ejecutar función principal
    main()
