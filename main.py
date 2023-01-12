import asyncio
from tasks.infinity_tasks import infinity_tasks


async def test():
    task = asyncio.create_task(infinity_tasks())
    await asyncio.gather(task)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
