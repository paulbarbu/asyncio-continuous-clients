import asyncio
import functools
import signal
import sys

should_exit = asyncio.Event()


def exit(signum, loop):
    should_exit.set()
    print('Exiting soon ...')


async def send(data, writer):
    while not should_exit.is_set():
        print(f'sending {data}')
        writer.write(data)
        await writer.drain()
        await asyncio.sleep(1)


async def client(name, host, port):
    reader, writer = await asyncio.open_connection(host, port)

    data = None

    print('conn opened')

    try:
        data = await reader.read(1024)
        print(f'Received data: {data}')

        if data == b'please start':
            await send(str(name).encode(), writer)

        print(f'client {name} has finished')
        writer.close()
        await writer.wait_closed()
    except ConnectionResetError:
        pass


async def main(num_clients, host, port):
    loop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGTERM, functools.partial(exit, signal.SIGTERM, loop))
    loop.add_signal_handler(signal.SIGINT, functools.partial(exit, signal.SIGINT, loop))

    tasks = (asyncio.create_task(client(vim READi, host, port)) for i in range(num_clients))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    num_clients = 1000
    host = '127.0.0.1'
    port = 4242

    if len(sys.argv) == 2:
        num_clients = int(sys.argv[1])

    print(f'running with {num_clients} clients')
    asyncio.run(main(num_clients, host, port))