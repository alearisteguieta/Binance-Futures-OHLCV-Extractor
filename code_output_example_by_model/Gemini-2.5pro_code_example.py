import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
import os

# --- Security and Environment Configuration ---
API_KEY = os.environ.get('BINANCE_API_KEY', '') 
API_SECRET = os.environ.get('BINANCE_API_SECRET', '')

# --- Requirement Constants ---
ASSETS = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'XRPUSDT']
TIMEFRAME = Client.KLINE_INTERVAL_1DAY 
START_DATE = '2021-01-01' 

# --- NEW ARRAY: Export Path ---
# The folder will be created in the same directory where you run the script.
OUTPUT_DIR = 'binance_data' 

# Function to get yesterday's date
def get_yesterday_date():
    """Calculates and returns yesterday's date as a 'YYYY-MM-DD' string."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

END_DATE = get_yesterday_date() 


# --- Main Data Extraction Function ---
def get_crypto_data(symbol: str, interval: str, start_str: str, end_str: str, output_path: str):
    """
    Extracts historical data from Binance futures API and exports it to a CSV
    at the specified path.
    
    Args:
        symbol (str): Asset ticker.
        interval (str): Timeframe.
        start_str (str): Start date.
        end_str (str): End date.
        output_path (str): Directory where the CSV will be saved.
        
    Returns:
        pd.DataFrame: Pandas DataFrame with the data or None.
    """
    # Initialize the client
    client = Client(API_KEY, API_SECRET)

    print(f"-> Extracting data for {symbol} from {start_str} to {end_str}...")

    try:
        # We use futures_historical_klines which handles pagination.
        klines = client.futures_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_str,
            end_str=end_str 
        )

    except Exception as e:
        print(f"Error getting data from API for {symbol}: {e}")
        return None

    # Expected columns from the API
    cols = [
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
        'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
        'Taker Buy Quote Asset Volume', 'Ignore'
    ]

    df = pd.DataFrame(klines, columns=cols)

    # --- Data Processing ---
    df = df[['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
    df.drop('Open Time', axis=1, inplace=True)
    df.set_index('Date', inplace=True)

    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    # 6. Export to CSV at the SPECIFIED PATH
    filename = f"{symbol}.csv"
    full_path = os.path.join(output_path, filename)
    
    df.to_csv(full_path)
    print(f"-> {symbol} data successfully saved to: {full_path}. Rows: {len(df)}")

    return df


# --- Main Script Execution ---
if __name__ == '__main__':
    print("--- Starting Binance Market Data Extraction ---")
    
    # 1. Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Output directory created: {OUTPUT_DIR}")
        
    print(f"Date Range: {START_DATE} to {END_DATE} (Timeframe: 1 Day)")
    print("-" * 50)

    for asset in ASSETS:
        # 2. Pass the output path to the function
        get_crypto_data(
            symbol=asset,
            interval=TIMEFRAME,
            start_str=START_DATE,
            end_str=END_DATE,
            output_path=OUTPUT_DIR
        )
        print("-" * 50)

    print("Data extraction finished :)")
