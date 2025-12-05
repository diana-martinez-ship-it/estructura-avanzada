import asyncio
import aiohttp

async def send_sale(session, i):
    payload = {'sale_id': f'S-{i}', 'product_id': 1, 'quantity_sold': 1}
    async with session.post('http://localhost:8001/sales', json=payload) as r:
        return await r.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_sale(session, i) for i in range(20)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print('Enviados', len(results))

if __name__ == '__main__':
    asyncio.run(main())
