import json

async def read_data(exchange):
    with open(f'{exchange}.json','r', encoding='utf-8') as f:
        return json.load(f)

async def write_data(exchange, data):
    with open(f'{exchange}.json','w', encoding='utf-8') as f:
        json.dump(data, f)