#!/usr/bin/env python3
"""
Binance Crypto Data Extractor
Extracts historical market data (candlestick) from the Binance API
and exports it to individual CSV files for each asset.
"""

import os
import pandas as pd
import requests
from datetime import datetime, timezone, timedelta

def criptodata(symbol):
    """
    Extracts historical candlestick data for a specific symbol from Binance
    
    Args:
        symbol (str): Asset symbol (e.g. 'BTCUSDT')
    
    Returns:
        pandas.DataFrame: DataFrame with processed historical data
    """
    
    # Base URL for Binance public API (no authentication required for historical data)
    base_url = "https://api.binance.com"
    
    # Define start and end dates
    start_date = datetime(2021, 1, 1, tzinfo=timezone.utc)
    end_date = datetime.now(timezone.utc) - timedelta(days=1)  # Previous day
    
    print(f"📈 Extracting data for {symbol} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    try:
        # Convert dates to timestamps in milliseconds (format required by Binance)
        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)
        
        # Get historical candlestick data using requests
        # Binance endpoint for klines (candlestick data)
        endpoint = f"{base_url}/api/v3/klines"
        
        # Parameters for the query
        params = {
            'symbol': symbol,
            'interval': '1d',  # Daily timeframe
            'startTime': start_timestamp,
            'endTime': end_timestamp,
            'limit': 1000  # Maximum per request
        }
        
        # Make API request
        response = requests.get(endpoint, params=params)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return None
        
        # Get JSON data
        klines = response.json()
        
        # Verify if data was obtained
        if not klines:
            print(f"❌ No data found for {symbol}")
            return None
        
        # Create DataFrame with obtained data
        # Klines structure: [timestamp, open, high, low, close, volume, close_time, ...]
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Select only necessary columns
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
        # Convert timestamp to readable date
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
        
        # Rename columns according to requirements
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Convert numeric values (they come as strings from the API)
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df[numeric_columns] = df[numeric_columns].astype(float)
        
        # Set date as index
        df.set_index('Date', inplace=True)
        
        # Sort by date (oldest first)
        df.sort_index(inplace=True)
        
        # Export to CSV
        filename = f"{symbol}.csv"
        full_path = os.path.abspath(filename)
        df.to_csv(filename)
        
        print(f"✅ Data successfully exported to:")
        print(f"   📁 Full path: {full_path}")
        print(f"   Records: {len(df)}")
        print(f"   Range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error processing {symbol}: {str(e)}")
        return None

def main():
    """
    Main function that processes all specified assets
    """
    
    print("🚀 Starting Binance data extraction")
    print("=" * 50)
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📄 CSV files will be saved in: {os.path.abspath('.')}")
    print("=" * 50)
    
    # List of assets to process
    assets = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT']
    
    successful_extractions = []
    failed_extractions = []
    
    # Process each asset
    for asset in assets:
        print(f"\n📊 Processing {asset}...")
        
        try:
            df = criptodata(asset)
            if df is not None:
                successful_extractions.append(asset)
            else:
                failed_extractions.append(asset)
        except Exception as e:
            print(f"❌ Unexpected error processing {asset}: {str(e)}")
            failed_extractions.append(asset)
    
    # Final summary
    print("\n" + "=" * 50)
    print("📈 EXTRACTION SUMMARY")
    print("=" * 50)
    
    if successful_extractions:
        print(f"✅ Successful extractions ({len(successful_extractions)}):")
        for asset in successful_extractions:
            full_path = os.path.abspath(f"{asset}.csv")
            print(f"   • {asset}.csv")
            print(f"     📁 {full_path}")
            print()
    
    if failed_extractions:
        print(f"❌ Failed extractions ({len(failed_extractions)}):")
        for asset in failed_extractions:
            print(f"   • {asset}")
    
    print(f"\nTotal processed: {len(assets)}")
    print(f"Successful: {len(successful_extractions)}")
    print(f"Failed: {len(failed_extractions)}")
    
    print("\n🎉 Data extraction finished :)")

if __name__ == "__main__":
    # Check dependencies
    try:
        import requests
        import pandas as pd
    except ImportError as e:
        print(f"❌ Error: Missing dependencies: {e}")
        print("   Install with: pip install requests pandas")
        exit(1)
    
    # Execute main function
    main()
