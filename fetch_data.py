import requests
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical'
params = {
    'symbol': 'ETH,BTC',
    'time_start': '2019-01-01',
    'time_end': '2022-01-01',
    'interval': 'daily',
}

# Set the API key as a header
headers = {
    'X-CMC_PRO_API_KEY': os.getenv('CMC_API')
}

# Make the API request and handle the response
response = requests.get(url, headers=headers, params=params)
data = response.json()

symbol = 'BTC'
quotes = data['data'][symbol][0]['quotes']

# df = pd.DataFrame(columns=['time', 'open', 'low', 'high', 'close', 'volume', 'market_cap'])
df = pd.DataFrame(columns=[ 'time','close'])


for i in range(0, len(quotes)):
    price_data = quotes[i]['quote']['USD']
    df = df.append({
        'time': price_data['timestamp'],
        # 'open': price_data['open'],
        # 'low': price_data['low'],
        # 'high': price_data['high'],
        'close': price_data['close']
        # 'volume': price_data['volume'],
        # 'market_cap': price_data['market_cap'],
    }, ignore_index=True)


df = df.set_index('time')
# print(df)
df.to_csv('data/BTC_data.csv')


