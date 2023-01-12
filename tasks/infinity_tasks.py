import asyncio

from tasks.parse_tradewagon import ParseTradeWagon


async def infinity_tasks():
    tradewagon_task = ParseTradeWagon()
    tasks = [
        tradewagon_task.update_traders(),
        tradewagon_task.update_ideas(),
    ]
    await asyncio.gather(*tasks)
