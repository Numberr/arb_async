import asyncio 
from aiohttp import ClientSession
from config import binance_api, okx_api, bybit_api
from utils import write_data


# Собираем и записываем данные в .json файл для каждой биржи
async def write_parsed_data(exchange): 
    urls = {
        'binance': binance_api,
        'okx': okx_api,
        'bybit': bybit_api
    }
    
    url = urls.get(exchange)
    if url == None:
        print('Неверная биржа')

    async with ClientSession() as session:
        try:
            async with session.get(url=url) as response:
                resp = await response.json()
                await write_data(exchange, resp)
                # with open(f'{exchange}.json','w', encoding='utf-8') as f:
                #     json.dump(resp, f)
        except Exception:
            print('Ошибка')

async def fetch_all_data(exchanges):
    tasks = []
    for exchange in exchanges:
        tasks.append(asyncio.create_task(write_parsed_data(exchange)))
        
    await asyncio.gather(*tasks)