import asyncio
import functools
import signal
import sys


async def exit(signum, loop, should_exit):
    should_exit.set()

    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    print(f'Cancelling {len(tasks)} remaining tasks')

    for task in tasks:
        task.cancel()

    print('Exiting soon ...')
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def handle_conn(should_exit, reader, writer):
    client = writer.get_extra_info('peername')
    if client:
        print(f'Handling connection from {client!r}')

    writer.write('please start'.encode())
    await writer.drain()

    data = await reader.read(1024)
    while not should_exit.is_set() and data != b'':
        print(f'Received {data} from {client!r}')
        data = await reader.read(1024)

    writer.close()
    await writer.wait_closed()


async def server(host, port, should_exit):
    server = await asyncio.start_server(functools.partial(handle_conn, should_exit), host, port)

    addr = server.sockets[0].getsockname()
    print(f'started server on {addr}')

    await should_exit.wait()
    server.close()
    await server.wait_closed()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 4242

    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])

    print(f'listening on {host}:{port}')

    loop = asyncio.get_event_loop()
    should_exit = asyncio.Event()

    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(exit(signal.SIGTERM, loop, should_exit)))
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(exit(signal.SIGINT, loop, should_exit)))
    loop.create_task(server(host, port, should_exit))

    try:
        loop.run_forever()
    finally:
        loop.close()
        print('bye')