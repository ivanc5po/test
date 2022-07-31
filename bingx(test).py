import time
import urllib.request
import json
import base64
import hmac

import os


try:
    import numpy as np
    import json
    import requests
except:
    os.system("pip install numpy")
    os.system("pip install json")
    os.system("pip install requests")

    import numpy as np
    import json
    import requests


APIURL = "https://api-swap-rest.bingbon.pro"
APIKEY = "APIKEY"
SECRETKEY = "SECRETKEY"

def get_price(coin):
    return float(requests.get('https://api-swap-rest.bingbon.pro/api/v1/market/getLatestPrice?symbol='+coin+'-USDT').text.split('"tradePrice":"')[1].split('"')[0])

def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(SECRETKEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256").digest()

def post(url, body):
    req = urllib.request.Request(url, data=body.encode("utf-8"), headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read()

def getBalance():
    paramsMap = {
        "apiKey": APIKEY,
        "timestamp": int(time.time()*1000),
        "currency": "USDT",
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/getBalance", "POST", paramsMap)))
    url = "%s/api/v1/user/getBalance" % APIURL
    return float(str(post(url, paramsStr)).split(',')[5].replace('"balance":', ''))

def closePositions(coin, amount):
    placeOrder(symbol=coin.upper()+"-USDT", side="Ask",volume=amount , tradeType="Market", action="Close", price=0)
    placeOrder(symbol=coin.upper()+"-USDT", side="Bid",volume=amount , tradeType="Market", action="Close", price=0)
    return "close"

def placeOrder(symbol, side, price, volume, tradeType, action):
    paramsMap = {
        "symbol": symbol,
        "apiKey": APIKEY,
        "side": side,
        "entrustPrice": price,
        "entrustVolume": volume,
        "tradeType": tradeType,
        "action": action,
        "timestamp": int(time.time()*1000),
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/trade", "POST", paramsMap)))
    url = "%s/api/v1/user/trade" % APIURL
    return post(url, paramsStr)



while True:
    #  getBalance() 抓取你錢包裡面的USDT數量
    print("你專業合約裡面的錢 : ", getBalance())
    #  get_price("幣種") 抓取貨幣價格
    print("現在BTC價格是 : ", get_price("BTC"))


    #  做空BTC, 市價單, 數量0.01
    #  placeOrder(symbol="BTC-USDT", side="Ask",volume=0.01 , tradeType="Market", action="Open", price=0)

    #  做多BTC, 市價單, 數量0.01
    #  placeOrder(symbol="BTC-USDT", side="Bid",volume=0.01 , tradeType="Market", action="Open", price=0)

    #  平倉BTC, 數量0.01
    #  closePositions("BTC", 0.01)

    time.sleep(5) #  等待5秒
