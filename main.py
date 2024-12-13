
import asyncio
from fetch_data import fetch_all_data
from process import comparison, search_matches, load_data
from sorting import sorting


async def main():
    exchanges = ['binance', 'okx', 'bybit']
    await fetch_all_data(exchanges)
    await sorting(exchanges)
    res_dict = await load_data(exchanges)
    data = await search_matches(res_dict)
    await comparison(data)

asyncio.run(main())