Python asyncio client-server example
====================================
The clients connect to the server and wait for data to be "confirmed" then they keep sending data until the server stops.
With added signal handling for proper closing of both client and server programs.

Inspired by the echo client-server example from the official docs.

Running
=======
Please use Python 3.7.4+

* client: `python3 ./client.py <number of clients>`
* server: `python3 ./server.py <listen addr> <port>`

Note: in order to be able to run with more than 1024 clients you'll have to raise the limit of opened files:
`ulimit -n 50000`


Future improvements
===================
* `argparse` should be used for command line arguments parsing


References
==========
https://realpython.com/async-io-python/#setting-up-your-environment
https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
https://docs.python.org/3/library/asyncio-stream.html
https://www.roguelynn.com/words/asyncio-graceful-shutdowns/
https://docs.python.org/3/library/asyncio-eventloop.html#set-signal-handlers-for-sigint-and-sigterm


License
=======
Copyright 2019 (c) Barbu Paul - Gheorghe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
