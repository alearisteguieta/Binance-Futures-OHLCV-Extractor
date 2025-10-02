#!/usr/bin/env python3
"""
Unit tests for _parse_klines_response.

Run:
    pytest testing_validation_by_model/test_parser.py
"""

import pandas as pd

from binance_ohlcv_extractor.extractor import _parse_klines_response


def test_parse_klines_response_basic():
    """
    Basic sanity check:
    - input: two sample klines (timestamps in ms and string numeric fields)
    - expected: DataFrame with DatetimeIndex and float numeric columns
    """
    sample = [
        [1609459200000, "100.0", "110.0", "90.0", "105.0", "123.45", 1609545599999, "0", 1, "0", "0", "0"],
        [1609545600000, "105.0", "115.0", "95.0", "110.0", "234.56", 1609631999999, "0", 1, "0", "0", "0"],
    ]

    df = _parse_klines_response(sample)

    assert isinstance(df.index, pd.DatetimeIndex)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df["open"].dtype == float
    assert len(df) == 2
