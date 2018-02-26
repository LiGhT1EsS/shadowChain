import asyncio
import logging
from functools import partial

from shadow import context
from shadow.log import logger
from shadow.protocols import in_protocol_chains, SCSProxyServer


def init():
    context.in_protocol_stack = [SCSProxyServer]
    context.out_protocol_stack = []
    context.logger = logger


if __name__ == '__main__':
    init()
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    logging.getLogger('asyncio').setLevel(logging.DEBUG)
    get_server_proto = partial(in_protocol_chains, loop)
    coro = loop.create_server(get_server_proto, '0.0.0.0', 9999)

    logger.debug(context.in_protocol_stack)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.shutdown_asyncgens()
    loop.stop()
    loop.close()
