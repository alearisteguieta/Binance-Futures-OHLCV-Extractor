import pandas as pd

from binance_ohlcv_extractor.extractor import _parse_klines_response

def test_parse_klines_response_basic():

sample = [

[1609459200000, "100.0", "110.0", "90.0", "105.0", "123.45", 1609545599999, "0", 1, "0", "0", "0"],

[1609545600000, "105.0", "115.0", "95.0", "110.0", "234.56", 1609631999999, "0", 1, "0", "0", "0"],

]

df = _parse_klines_response(sample)

assert isinstance(df.index, pd.DatetimeIndex)

assert list(df.columns) == ["open", "high", "low", "close", "volume"]

assert df["open"].dtype == float

assert len(df) == 2
