import asyncio, pythrust

loop = asyncio.get_event_loop()
api = pythrust.API(loop)

asyncio.ensure_future(api.spawn())
asyncio.ensure_future(api.window({ 'root_url': 'http://google.com' }).show())

loop.run_forever()
