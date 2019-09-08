import asyncio
import functools
import signal
import sys


def exit(signum, loop, should_exit):
    should_exit.set()
    print('Exiting soon ...')


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


async def main(host, port):
    loop = asyncio.get_running_loop()
    should_exit = asyncio.Event()

    loop.add_signal_handler(signal.SIGTERM, functools.partial(exit, signal.SIGTERM, loop, should_exit))
    loop.add_signal_handler(signal.SIGINT, functools.partial(exit, signal.SIGINT, loop, should_exit))
    await server(host, port, should_exit)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 4242

    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])

    print(f'listening on {host}:{port}')
    asyncio.run(main(host, port))