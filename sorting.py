import json
import asyncio
from utils import write_data

# Убираем из .json файлов все пары, цена которых представлена не в usdt
async def usdt_sorting(exc): 
    with open(f'{exc}.json', 'r', encoding='utf-8') as f:
        if exc == 'okx':
            exc_data = json.load(f)['data']
        if exc == 'binance':
            exc_data = json.load(f)
        if exc == 'bybit':
            exc_data = json.load(f)['result']['list']

    exc_sorted = []

    if exc == 'okx':
        for dict in exc_data:
            if dict['instId'][-4:] == 'USDT':
                exc_sorted.append(dict)
    
    if exc == 'binance' or exc == 'bybit':
        for dict in exc_data:
            if dict['symbol'][-4:] == 'USDT':
                exc_sorted.append(dict)

    await write_data(exc, exc_sorted)


async def sorting(exchanges):
    tasks = []
    for exc in exchanges:
        tasks.append(asyncio.create_task(usdt_sorting(exc)))

    await asyncio.gather(*tasks)