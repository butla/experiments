# test.py
# python 3.8.1

import asyncio
import aiohttp


async def non_working_solution():
    task = asyncio.create_task(registerit())


async def working_solution():
    await registerit()


async def registerit():
    async with aiohttp.ClientSession() as session:
        url="https://google.com"
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        response = await session.get(url, headers=headers)
        print(response)


async def main():
    print('Running working solution')
    await working_solution()
    print('Running NON-working solution')
    await non_working_solution()

    # THE FIX
    # =======
    time_to_sleep = 5
    print('Waiting for', time_to_sleep, 'seconds for the output of the non-working solution')
    await asyncio.sleep(time_to_sleep)
    # =======


if __name__ == '__main__':
    asyncio.run(main())
