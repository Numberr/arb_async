import asyncio
from utils import read_data
from config import EXPECTED_DIFFERENCE
import json


# Создаем словарь с ключами в виде бирж и значениями - их отсортированными данными
async def load_data(exchanges):
    tasks = []
    for exchange in exchanges:  
        task = asyncio.create_task(read_data(exchange))
        tasks.append(task)
    results = await asyncio.gather(*tasks) # возвращает список результатов

    result_dict = {}
    for exchange, result in zip(exchanges, results):
        result_dict[exchange] = result
    return result_dict # Вернет словарь где сибржи будут совпадать с тем что щас в файлах жсон

# Создаем список словарей, в каждом из которых будет информация о ценах монеты на всех биржах
async def search_matches(dict_):
    binance_coins = {}
    for pair in dict_['binance']:
        coin = pair['symbol'][:-4]
        binance_coins[coin] = float(pair['price'])

    okx_coins = {}
    for pair in dict_['okx']:
        coin = pair['instId'][:-5]
        okx_coins[coin] = float(pair['last'])

    bybit_coins = {}
    for pair in dict_['bybit']:
        coin = pair['symbol'][:-4]
        bybit_coins[coin] = float(pair['lastPrice'])

    longest = max([binance_coins, okx_coins, bybit_coins], key=len)
    final_prices = []
    for key in longest.keys():
        dict_ = {}
        if key in binance_coins and key in okx_coins and key in bybit_coins:
            dict_['coin'] = key
            dict_['binance_price'] = binance_coins[key]
            dict_['okx_price'] = okx_coins[key]
            dict_['bybit_price'] = bybit_coins[key]
            final_prices.append(dict_)

    return final_prices

# Сравниваем цены в каждом словаре
async def comparison(data):
    for dict_ in data:
        prices = [value for key, value in dict_.items() if 'price' in key]
        max_price = max(prices)
        min_price = min(prices)
        max_price_exchange = [k for k, v in dict_.items() if v == max_price]
        min_price_exchange = [k for k, v in dict_.items() if v == min_price]
        try:
            difference = max_price / min_price * 100 - 100 # Разница в %
            if difference > EXPECTED_DIFFERENCE:
                    print(f"Найдена разница ({difference}%), монета {dict_['coin']}, "+
                    f"цена покупки {min_price} на бирже {min_price_exchange[0][:-6]}, "+
                    f"цена продажи {max_price} на бирже {max_price_exchange[0][:-6]}")
        except ZeroDivisionError:
            print(f"Не удалось поссчитать разницу так как цена на монету {dict_['coin']} равна 0.")