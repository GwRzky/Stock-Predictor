import requests
import pandas as pd
from flask import current_app
import json
from datetime import datetime, timedelta
import yfinance as yf

INDEX_SYMBOLS = [
    '^GSPC', '^DJI', '^IXIC', '^NYA', '^RUT', '^XAX', '^VIX', '^XMI', '^SOX', '^NDX', '^SP100', '^SP1500',
    '^SP400', '^SP600', '^W5000', '^FTSE', '^GDAXI', '^FCHI', '^N100', '^AEX', '^STOXX50E', '^IBEX', '^SSMI',
    '^N225', '^TOPX', '^HSI', '^TWII', '^STI', '^AXJO', '^BSESN', '^NSEI', '^KS11', '^BVSP', '^MXX', '^IPSA',
    '^MERVAL', '^DJT', '^DJU', '^DJUSHC', '^DJUSFN', '^DJUSEN', '^DJUSRE', '^DJUSIN', '^DJUSIT', '^IXHC',
    '^IXF', '^IXE', '^IXRE'
]

def fetch_top_indices(limit=10, sort_by='change_percent'):
    results = []

    for symbol in INDEX_SYMBOLS:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")

            if len(hist) >= 2:
                today = hist.iloc[-1]
                yesterday = hist.iloc[-2]
                if 'Close' in today and pd.notna(today['Close']):
                    price = today['Close']
                    change_percent = ((today['Close'] - yesterday['Close']) / yesterday['Close']) * 100
                else:
                    price = None
                    change_percent = 0

            else:
                price = None
                change_percent = 0

            results.append({
                'symbol': symbol,
                'name': ticker.info.get('shortName', symbol),
                'price': round(price, 2) if price else None,
                'change_percent': round(change_percent, 2),
            })

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            results.append({
                'symbol': symbol,
                'name': symbol,
                'price': None,
                'change_percent': 0
            })

    return sorted(results, key=lambda x: x.get(sort_by) or 0, reverse=True)[:limit]

def fetch_top_cryptocurrencies(limit=5):
    """
    Dynamically fetch top cryptocurrencies from CoinGecko API
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        cryptos = []
        for crypto in data:
            cryptos.append({
                'symbol': crypto['symbol'].upper(),
                'function': 'DIGITAL_CURRENCY_DAILY',
                'market': 'USD',
                'name': crypto['name'],
                'current_price': crypto['current_price'],
                'market_cap': crypto['market_cap'],
                'change_percent': crypto['price_change_percentage_24h']
            })
        
        return cryptos
    except Exception as e:
        print(f"Error fetching cryptocurrencies: {str(e)}")
        return [
            {'symbol': 'BTC', 'function': 'DIGITAL_CURRENCY_DAILY', 'market': 'USD', 'name': 'Bitcoin'},
            {'symbol': 'ETH', 'function': 'DIGITAL_CURRENCY_DAILY', 'market': 'USD', 'name': 'Ethereum'},
            {'symbol': 'SOL', 'function': 'DIGITAL_CURRENCY_DAILY', 'market': 'USD', 'name': 'Solana'}
        ][:limit]

def get_market_data(symbol='AAPL'):
    """
    Fetch market data for a specific symbol using Alpha Vantage API
    """
    api_key = current_app.config['ALPHA_VANTAGE_API_KEY']
    base_url = 'https://www.alphavantage.co/query'
    
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'compact',
        'apikey': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if 'Error Message' in data:
            return {'error': data['Error Message']}
            
        overview_params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': api_key
        }
        overview_response = requests.get(base_url, params=overview_params)
        overview_data = overview_response.json()
        
        time_series = data.get('Time Series (Daily)', {})
        dates = sorted(time_series.keys(), reverse=True)[:7]
        
        processed_data = {
            'dates': dates,
            'prices': [float(time_series[date]['4. close']) for date in dates],
            'volumes': [int(time_series[date]['5. volume']) for date in dates],
            'overview': overview_data,
            'raw': data
        }
        
        return processed_data
    except Exception as e:
        return {'error': str(e)}

def get_crypto_data(symbol='BTC', market='USD'):
    """
    Fetch cryptocurrency data using Alpha Vantage API
    """
    api_key = current_app.config['ALPHA_VANTAGE_API_KEY']
    base_url = 'https://www.alphavantage.co/query'
    
    params = {
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': symbol,
        'market': market,
        'apikey': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if 'Error Message' in data:
            return {'error': data['Error Message']}
            
        time_series = data.get('Time Series (Digital Currency Daily)', {})
        dates = sorted(time_series.keys(), reverse=True)[:7]
        
        processed_data = {
            'dates': dates,
            'prices': [float(time_series[date]['4a. close (USD)']) for date in dates],
            'volumes': [float(time_series[date]['5. volume']) for date in dates],
            'asset_type': 'crypto',
            'symbol': symbol,
            'name': f"{symbol}/USD",
            'raw': data
        }
        
        return processed_data
    except Exception as e:
        return {'error': str(e)}

def get_general_market_data(index_limit=4, crypto_limit=3):
    """
    Fetch data for major market indices and cryptocurrencies
    """
    top_indices = fetch_top_indices(index_limit)
    top_cryptos = fetch_top_cryptocurrencies(crypto_limit)
    
    results = {'indices': [], 'cryptos': []}
    
    for index in top_indices:
        if 'price' in index and 'change_percent' in index:
            results['indices'].append({
                'name': index['name'],
                'symbol': index['symbol'],
                'current_price': index['price'],
                'change_percent': index['change_percent'],
                'trend': 'up' if index['change_percent'] > 0 else 'down',
            })
        else:
            data = get_market_data(index['symbol'])
            if 'error' not in data and data.get('prices'):
                prices = data.get('prices', [])
                
                if len(prices) > 1:
                    change = ((prices[0] - prices[-1]) / prices[-1]) * 100
                else:
                    change = 0
                    
                results['indices'].append({
                    'name': index['name'],
                    'symbol': index['symbol'],
                    'current_price': prices[0] if prices else None,
                    'change_percent': change,
                    'trend': 'up' if change > 0 else 'down',
                })
    
    for crypto in top_cryptos:
        if 'current_price' in crypto and 'change_percent' in crypto:
            results['cryptos'].append({
                'name': crypto['name'],
                'symbol': crypto['symbol'],
                'current_price': crypto['current_price'],
                'change_percent': crypto['change_percent'],
                'trend': 'up' if crypto['change_percent'] > 0 else 'down',
            })
        else:
            data = get_crypto_data(crypto['symbol'])
            if 'error' not in data and data.get('prices'):
                prices = data.get('prices', [])
                
                if len(prices) > 1:
                    change = ((prices[0] - prices[-1]) / prices[-1]) * 100
                else:
                    change = 0
                    
                results['cryptos'].append({
                    'name': crypto['name'],
                    'symbol': crypto['symbol'],
                    'current_price': prices[0] if prices else None,
                    'change_percent': change,
                    'trend': 'up' if change > 0 else 'down',
                })
    
    return results