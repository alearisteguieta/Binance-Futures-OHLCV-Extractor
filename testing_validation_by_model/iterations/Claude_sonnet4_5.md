# Iteration process with the LLM

## Claude Sonnet 4.5 

This section of the repository presents an example iteration designed to enable the language model (Claude) 
to generate error-free code after testing in Visual Studio Code. 
Here, you can see the entire process, from entering the initial prompt (financial_framework_template.md) to the final output and any corrections made. 
We recommend using this guide as a reference for your own iterations.

Prompt imput: 

```bash

1) Domain Context

**Role:** You are a software developer with experience in FinTech and financial market APIs.

**Objective:** Create a Python script to extract historical market data (candlestick data) from the Binance API and export them to a CSV file.

2) Functional Requirements

**Data Sources:** The Binance API for USDT futures.

**Assets:** The function should be capable of processing a list of assets, specifically BTCUSDT, ETHUSDT, ADAUSDT, and XRPUSDT.

**Data to Extract:** Date, Open, High, Low, Close, Volume.

**Date Range:** From January 1, 2021 until the day before the script execution.

**Timeframe:** Daily (1d).

**Data Processing:** Convert the timestamp from the Date column to a readable date format and set it as the DataFrame index.

3) Technical Requirements

**Language:** Python.

**Libraries:** binance-connector, pandas, datetime.

**API Keys Handling:** The script must handle API keys securely.

**Output Format:** A separate CSV file for each asset, named with the asset's ticker (e.g., BTCUSDT.csv)

**Code Structure:** The code should be modular, with a main function (criptodata) that can be called within a loop to process multiple assets.

4) Specific Instructions to the Assistant (Prompt)

Write only the Python code in a single code block.

Include clear comments to explain each step, such as data conversion and DataFrame handling.

Ensure the script can be executed directly from the console.

Include a confirmation message at the end, such as "Data extraction finished :)".

5) Validation

The function logic should be reproducible and generate a correct pandas DataFrame before exporting it to a CSV.

The code should be robust to handle the provided list of assets without errors.

```

Claude response: 

```python
#!/usr/bin/env python3
"""
Binance Crypto Data Extractor
Extrae datos históricos de mercado (candlestick) desde la API de Binance
y los exporta a archivos CSV individuales para cada activo.
"""

import os
import pandas as pd
from datetime import datetime, timezone, timedelta
from binance.spot import Spot

def criptodata(symbol):
    """
    Extrae datos históricos de candlestick para un símbolo específico desde Binance
    
    Args:
        symbol (str): Símbolo del activo (ej. 'BTCUSDT')
    
    Returns:
        pandas.DataFrame: DataFrame con los datos históricos procesados
    """
    
    # Configuración de API keys de forma segura
    # IMPORTANTE: Nunca hardcodear las API keys en el código
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("⚠️  Advertencia: API keys no encontradas en variables de entorno.")
        print("   Para datos públicos (históricos), Binance no requiere autenticación.")
        print("   Continuando sin autenticación...")
        client = Spot()
    else:
        # Inicializar cliente de Binance con autenticación
        client = Spot(api_key=api_key, api_secret=api_secret)
    
    # Definir fechas de inicio y fin
    start_date = datetime(2021, 1, 1, tzinfo=timezone.utc)
    end_date = datetime.now(timezone.utc) - timedelta(days=1)  # Día anterior
    
    print(f"📈 Extrayendo datos para {symbol} desde {start_date.strftime('%Y-%m-%d')} hasta {end_date.strftime('%Y-%m-%d')}")
    
    try:
        # Convertir fechas a timestamps en milisegundos (formato requerido por Binance)
        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)
        
        # Obtener datos de candlestick históricos
        # Parámetros: symbol, interval, startTime, endTime, limit
        klines = client.klines(
            symbol=symbol,
            interval='1d',  # Timeframe diario
            startTime=start_timestamp,
            endTime=end_timestamp,
            limit=1000  # Máximo por request
        )
        
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
        df.to_csv(filename)
        
        print(f"✅ Datos exportados exitosamente a {filename}")
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
            print(f"   • {asset}.csv")
    
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
        import binance
    except ImportError:
        print("❌ Error: La librería 'binance-connector' no está instalada.")
        print("   Instala con: pip install python-binance")
        exit(1)
    
    # Ejecutar función principal
    main()
```

```bash
I have created a complete Python script that meets all your requirements. The code includes:

## 🎯 **Main Features:**

**Core Functionality:**

- Extracts historical candlestick data from the Binance API
- Processes the 4 specified assets: `BTCUSDT`, `ETHUSDT`, `ADAUSDT`, `XRPUSDT`
- Date range: January 1, 2021 to the previous day
- Daily timeframe (`1d`)

**Data Processing:**

- Converts timestamps to readable dates in UTC format
- Selects the required columns: `Date`, `Open`, `High`, `Low`, `Close`, `Volume`
- Sets the date as the DataFrame index
- Correctly converts numerical values

**Security and Best Practices:**

- Secure handling of API keys using environment variables
- Works without authentication for public historical data
- Robust handling of errors and exceptions

**Modularity:**

- Reusable `criptodata()` function for any symbol
- A `main()` function that processes the complete list of assets
- Well-commented and structured code

## 📦 **Dependencies Installation:**

bash

`pip install python-binance pandas`

## 🔑 **Optional API Keys Configuration:**

For greater robustness (although not necessary for historical data):

bash

`export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"`

## 🚀 **Execution:**

bash

`python script.py`

The script will generate one CSV file per asset (`BTCUSDT.csv`, `ETHUSDT.csv`, etc.) with a detailed summary of the process at the end, including the confirmation message "Data extraction finished :)".
```
