import asyncio


async def run_server():
    port = 8000
    server = await asyncio.start_server(
        handle_connection,
        '127.0.0.1',
        port,
    )
    print('Ready for connections on port', port)

    async with server:
        await server.serve_forever()


async def handle_connection(reader, writer):
    print('Connected')
    data = await reader.read(100)
    print('Received:', data)

    writer.write("You've sent: ".encode() + data)
    print('responded')
    await writer.drain()

    print('closing connection')
    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    asyncio.run(run_server())
