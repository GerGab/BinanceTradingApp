import requests
import json
import pandas as pd

filter = ["usdt","wbtc","busd","usdc","dai"]
geckoURL = "https://api.coingecko.com/api/v3"
market_endpoint = "/coins/markets?vs_currency="
currency_id = "usd"
def GetMarketCap(qty):
    response = requests.get(geckoURL+market_endpoint+currency_id)
    response = response.json()
    coins = []
    for i in response:
        coins.append(i["symbol"])
    df = pd.DataFrame({"coins":coins},index=coins)
    df = df.drop(filter)
    coins = df[:qty].index
    new_coins = []
    for i in range(len(coins)):
        new_coins.append(coins[i].upper()+"USDT")
    return(new_coins[:qty])

if __name__ == '__main__':
    coins = GetMarketCap(50)
    print(coins)
